from flask import Flask, request, Response
from flask_restful import Api, Resource, fields, marshal_with, marshal
from flask_cors import CORS
from mongoengine import connect, Document, StringField, IntField
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})
api = Api(app)

# MongoDB connection
<<<<<<< HEAD
mongo_uri = os.environ.get('MONGO_URI', 'MONGO_URI')
=======
<<<<<<< HEAD
mongo_uri = os.environ.get('MONGO_URI', 'MONGO_URI')
=======
mongo_uri = os.environ.get('MONGO_URI', 'mongodb+srv://Mohammad1999:o2bTE0PjajxuPhYP@cluster0.obssh08.mongodb.net/')
>>>>>>> 344dda6 (chore: initial implement backend code)
>>>>>>> f3baf79 (chore: fix the content)
connect(host=mongo_uri)

def error_response(message, status_code,):
    return {'message': message }, status_code

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
    def post(self):
        username = request.json.get('username')
        if not username:
            return error_response('Username is required', 400)
        
        if len(username) > 8:
            return error_response('Username length must be lower than 9 char', 400)
        
        try:
            user = User(username=username).save()
            return marshal({
                'message': 'User created successfully', 
                'id': str(user.id), 
                'username': str(user.username)
            }, message_fields), 201
        except Exception as e:
            return error_response(f'Error creating user {str(e)}', 400)

class SendScore(Resource):
    def post(self):
        id = request.json.get('id')
        score = request.json.get('score')
        
        if not id or score is None:
            return error_response('id and score are required', 400)
        
        try:
            user = User.objects(id=id).first()
            if user:
                if int(user.score) > int(score):
                    return error_response('Bad request, score is not valid', 400)
                user.score = score
                user.save()
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

if __name__ == '__main__':
    app.run(debug=True)