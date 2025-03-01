import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for application settings."""

    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/users_db")
