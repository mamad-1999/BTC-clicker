import logging
from flask import request
from flask_restful import Resource, marshal_with, marshal

from models import User
from serializers import user_fields, message_fields
from utils import error_response, sanitize_username


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
        return limiter.limit("2 per minute")(cls.post)

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
