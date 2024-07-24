from flask import Flask, request
from flask_restful import Api, Resource, fields, marshal_with, marshal
from mongoengine import connect, Document, StringField, IntField
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
from flask_cors import CORS
from redis import Redis
import os
import logging
import re
import unicodedata

load_dotenv()

MONGO_URL = os.getenv('MONGO_URL')

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})
api = Api(app)


def error_response(message, status_code,):
    return {'message': message}, status_code


redis_client = Redis(host='localhost', port=6379, db=0)
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    storage_uri="redis://localhost:6379"
)

mongo_uri = os.environ.get('MONGO_URI', {MONGO_URL})
try:
    connect(host=mongo_uri)
except Exception as e:
    app.logger.error(f"Failed to connect to MongoDB: {str(e)}")

# User Model


class User(Document):
    username = StringField(required=True)
    score = IntField(default=0)

    meta = {
        'collection': 'users',
    }


# Resource fields for marshalling
user_fields = {
    'username': fields.String,
    'score': fields.Integer
}

message_fields = {
    'message': fields.String,
    'id': fields.String,
    'username': fields.String
}


def error_response(message, status_code,):
    return {'message': message}, status_code

# API Resources


class GetUsers(Resource):
    @marshal_with(user_fields)
    def get(self):
        try:
            top_users = User.objects.order_by('-score').limit(50)
            if top_users:
                return list(top_users)
            else:
                return error_response('Users Not Found', 400)
        except Exception as e:
            return error_response(f'Error Get All users {str(e)}', 400)


class CreateUser(Resource):
    decorators = [limiter.limit("2 per minute")]

    def sanitize_username(self, username):
        username = username.strip()
        username = username.replace(' ', '_')
        username = re.sub(r'[^\w\s-]', '', username)
        username = ''.join(c for c in unicodedata.normalize('NFD', username)
                           if unicodedata.category(c) != 'Mn')
        username = username.lower()

        return username

    def post(self):
        username = request.json.get('username')
        if not username:
            return error_response('Username is required', 400)

        # Sanitize the username
        sanitized_username = self.sanitize_username(username)

        if len(sanitized_username) < 3:
            return error_response('Username must be at least 3 characters long', 400)

        if len(sanitized_username) > 8:
            return error_response('Username length must be lower than 9 characters', 400)

        try:
            # Check if username already exists
            if User.objects(username=sanitized_username).first():
                return error_response('Username already exists', 400)

            user = User(username=sanitized_username).save()
            app.logger.info(f"User created: {user.username}")
            return marshal({
                'message': 'User created successfully',
                'id': str(user.id),
                'username': str(user.username)
            }, message_fields), 201
        except Exception as e:
            app.logger.error(f"Error creating user: {str(e)}")
            return error_response(f'Error creating user: {str(e)}', 400)


class SendScore(Resource):
    def post(self):
        id = request.json.get('id')
        score = request.json.get('score')

        if not id or score is None:
            return error_response('id and score are required', 400)

        try:
            score = int(request.json.get('score'))
        except ValueError:
            return error_response('score must be a valid integer', 400)

        try:
            user = User.objects(id=id).first()
            if user:
                if user.score > score:
                    return error_response('Bad request, score is not valid', 400)
                user.score = score
                user.save()
                app.logger.info(
                    f"Score updated for user {user.username}: {score}")
                return marshal({
                    'message': 'Score updated successfully',
                    'id': str(user.id),
                    'username': str(user.username)
                }, message_fields), 200
            else:
                return error_response('User Not Found', 400)
        except Exception as e:
            return error_response(f'Error updating score {str(e)}', 400)


# API routes
api.add_resource(GetUsers, '/get-users')
api.add_resource(CreateUser, '/create-user')
api.add_resource(SendScore, '/send-score')

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    app.run(debug=True)
