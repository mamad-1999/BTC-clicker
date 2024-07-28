from flask_restful import fields

user_fields = {
    'username': fields.String,
    'score': fields.Integer
}

message_fields = {
    'message': fields.String,
    'id': fields.String,
    'username': fields.String
}
