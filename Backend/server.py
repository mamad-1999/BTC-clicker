import os
import logging
import re
import unicodedata
from typing import Dict, Any

from flask import Flask, request
from flask_restful import Api, Resource, fields, marshal_with, marshal
from mongoengine import connect, Document, StringField, IntField
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
from flask_cors import CORS
from redis import Redis

# Load environment variables
load_dotenv()

# Configuration


class Config:
    MONGO_URL = os.getenv('MONGO_URL')
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    REDIS_DB = 0
    CORS_ORIGIN = "http://localhost:5173"
    RATE_LIMIT = "2 per minute"

# Database models


class User(Document):
    username = StringField(required=True)
    score = IntField(default=0)

    meta = {
        'collection': 'users',
    }


# Serialization fields
user_fields = {
    'username': fields.String,
    'score': fields.Integer
}

message_fields = {
    'message': fields.String,
    'id': fields.String,
    'username': fields.String
}

# Utility functions


def error_response(message: str, status_code: int) -> Dict[str, Any]:
    return {'message': message}, status_code


def sanitize_username(username: str) -> str:
    username = username.strip()
    username = username.replace(' ', '_')
    username = re.sub(r'[^\w\s-]', '', username)
    username = ''.join(c for c in unicodedata.normalize('NFD', username)
                       if unicodedata.category(c) != 'Mn')
    return username.lower()

# API Resources


class GetUsers(Resource):
    @marshal_with(user_fields)
    def get(self):
        try:
            top_users = User.objects.order_by('-score').limit(50)
            return list(top_users) if top_users else error_response('Users Not Found', 400)
        except Exception as e:
            return error_response(f'Error Get All users {str(e)}', 400)


class CreateUser(Resource):
    @classmethod
    def add_rate_limit(cls, limiter):
        return limiter.limit(Config.RATE_LIMIT)(cls.post)

    def post(self):
        username = request.json.get('username')
        if not username:
            return error_response('Username is required', 400)

        sanitized_username = sanitize_username(username)

        if len(sanitized_username) < 3:
            return error_response('Username must be at least 3 characters long', 400)
        if len(sanitized_username) > 8:
            return error_response('Username length must be lower than 9 characters', 400)

        try:
            if User.objects(username=sanitized_username).first():
                return error_response('Username already exists', 400)

            user = User(username=sanitized_username).save()
            logging.info(f"User created: {user.username}")
            return marshal({
                'message': 'User created successfully',
                'id': str(user.id),
                'username': str(user.username)
            }, message_fields), 201
        except Exception as e:
            logging.error(f"Error creating user: {str(e)}")
            return error_response(f'Error creating user: {str(e)}', 400)


class SendScore(Resource):
    def post(self):
        id = request.json.get('id')
        score = request.json.get('score')

        if not id or score is None:
            return error_response('id and score are required', 400)

        try:
            score = int(score)
        except ValueError:
            return error_response('score must be a valid integer', 400)

        try:
            user = User.objects(id=id).first()
            if not user:
                return error_response('User Not Found', 400)
            if user.score > score:
                return error_response('Bad request, score is not valid', 400)

            user.score = score
            user.save()
            logging.info(f"Score updated for user {user.username}: {score}")
            return marshal({
                'message': 'Score updated successfully',
                'id': str(user.id),
                'username': str(user.username)
            }, message_fields), 200
        except Exception as e:
            return error_response(f'Error updating score {str(e)}', 400)

# Application setup


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": Config.CORS_ORIGIN}})
    api = Api(app)

    # Database connection
    try:
        connect(host=Config.MONGO_URL)
    except Exception as e:
        logging.error(f"Failed to connect to MongoDB: {str(e)}")

    # Redis and Limiter setup
    redis_client = Redis(host=Config.REDIS_HOST,
                         port=Config.REDIS_PORT, db=Config.REDIS_DB)
    limiter = Limiter(
        key_func=get_remote_address,
        app=app,
        storage_uri=f"redis://{Config.REDIS_HOST}:{Config.REDIS_PORT}"
    )

    # API routes
    api.add_resource(GetUsers, '/get-users')
    api.add_resource(CreateUser, '/create-user')
    CreateUser.add_rate_limit(limiter)  # Apply rate limiting to CreateUser
    api.add_resource(SendScore, '/send-score')

    return app


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app = create_app()
    app.run(debug=True)
