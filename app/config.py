import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for application settings.

    Attributes:
        MONGODB_URI (str): MongoDB connection string. Defaults to local MongoDB
                          instance if not specified in environment variables.
    """

    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/users_db")
