from flask import Flask, request
from flask_restful import Api, Resource
from mongoengine import connect, Document, StringField, IntField
from bson.json_util import dumps
import os

app = Flask(__name__)
api = Api(app)

# MongoDB connection
mongo_uri = os.environ.get('MONGO_URI', 'your_mongodb_atlas_connection_string')
connect(host=mongo_uri)

# User Model
class User(Document):
    username = StringField(required=True, unique=True)
    score = IntField(default=0)

    meta = {
        'collection': 'users',
        'indexes': [
            {'fields': ['score'], 'order': -1}  # Index for efficient sorting
        ]
    }

    def to_dict(self):
        return {
            'username': self.username,
            'score': self.score
        }

# API Resources
class GetUsers(Resource):
    def get(self):
        top_users = User.objects.order_by('-score').limit(10)
        return dumps([user.to_dict() for user in top_users])

class CreateUser(Resource):
    def post(self):
        username = request.json.get('username')
        if not username:
            return {'message': 'Username is required'}, 400
        
        try:
            user = User(username=username).save()
            return {'message': 'User created successfully', 'id': str(user.id)}, 201
        except Exception as e:
            return {'message': f'Error creating user: {str(e)}'}, 400

class SendScore(Resource):
    def post(self):
        username = request.json.get('username')
        score = request.json.get('score')
        
        if not username or score is None:
            return {'message': 'Username and score are required'}, 400
        
        try:
            user = User.objects(username=username).first()
            if user:
                user.score = score
                user.save()
                return {'message': 'Score updated successfully'}, 200
            else:
                User(username=username, score=score).save()
                return {'message': 'New user created with score'}, 201
        except Exception as e:
            return {'message': f'Error updating score: {str(e)}'}, 400

# API routes
api.add_resource(GetUsers, '/get-users')
api.add_resource(CreateUser, '/create-user')
api.add_resource(SendScore, '/send-score')

if __name__ == '__main__':
    app.run(debug=True)