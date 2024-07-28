from mongoengine import Document, StringField, IntField


class User(Document):
    username = StringField(required=True)
    score = IntField(default=0)

    meta = {
        'collection': 'users',
    }
