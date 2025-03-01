import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for application settings."""

    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    MONGODB_DBNAME = os.getenv("MONGODB_DBNAME", "users_db")
    RATELIMIT_ENABLED = os.getenv("RATELIMIT_ENABLED", "True")
    RATELIMIT_HEADERS_ENABLED = os.getenv("RATELIMIT_HEADERS_ENABLED", "False")

    RATELIMIT_STORAGE_URI = MONGODB_URI
