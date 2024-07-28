import logging
from flask import Flask
from flask_restful import Api
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
from mongoengine import connect
from redis import Redis

from config import Config
from resources import GetUsers, CreateUser, SendScore


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
