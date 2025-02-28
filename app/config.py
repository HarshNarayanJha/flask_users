import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/users_db")
