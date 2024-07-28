import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    MONGO_URL = os.getenv('MONGO_URL')
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    REDIS_DB = 0
    CORS_ORIGIN = "http://localhost:5173"
    RATE_LIMIT = "2 per minute"
