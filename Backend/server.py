from flask import Flask, request
from flask_restful import Api, Resource, fields, marshal_with
from mongoengine import connect, Document, StringField, IntField
import os

app = Flask(__name__)
api = Api(app)

# MongoDB connection
mongo_uri = os.environ.get('MONGO_URI', 'MONGO_URI')
connect(host=mongo_uri)

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
    'id': fields.String
}

# API Resources
class GetUsers(Resource):
    @marshal_with(user_fields)
    def get(self):
        try:
            top_users = User.objects.order_by('-score').limit(10)
            if top_users:
                return list(top_users)
            else:
                return {'message': 'Users Not Found'}, 400
        except Exception as e:
            return {'message': f'Error Get All users: {str(e)}'}, 400

class CreateUser(Resource):
    @marshal_with(message_fields)
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
    @marshal_with(message_fields)
    def post(self):
        id = request.json.get('id')
        score = request.json.get('score')
        
        if not id or score is None:
            return {'message': 'id and score are required'}, 400
        
        try:
            user = User.objects(id=id).first()
            if user:
                user.score = score
                user.save()
                return {'message': 'Score updated successfully', 'id': str(user.id)}, 200
            else:
                return {'message': 'User Not Found', id: 'Not Found'}, 404
        except Exception as e:
            return {'message': f'Error updating score: {str(e)}'}, 400

# API routes
api.add_resource(GetUsers, '/get-users')
api.add_resource(CreateUser, '/create-user')
api.add_resource(SendScore, '/send-score')

if __name__ == '__main__':
    app.run(debug=True)