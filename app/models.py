from typing import Any, Dict, Generic, Type, TypeVar

from flask_bcrypt import check_password_hash, generate_password_hash
from mongoengine import Document, EmailField, QuerySet, StringField

U = TypeVar("U", bound=Document)


class QuerySetManager(Generic[U]):
    def __get__(self, instance: object, cls: Type[U]) -> QuerySet:
        return QuerySet(cls, cls._get_collection())


class User(Document):
    """
    User model representing application users.

    This Document class defines the schema for user data stored in MongoDB.
    """

    meta = {"collection": "users"}

    name = StringField(required=True, max_length=30)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True, min_length=8)

    objects = QuerySetManager["User"]()

    def hash_password(self):
        """
        Hash the user's password using bcrypt.

        This method should be called before saving a new user to the database or when updating an existing user's password.
        """
        self.password = generate_password_hash(self.password).decode("utf8")

    def check_password(self, password: str) -> bool:
        """
        Verify if the provided password matches the stored hash.

        Args:
            password: The plaintext password to check

        Returns:
            True if the password matches, False otherwise
        """
        return check_password_hash(self.password, password)

    def to_json(self, *args, **kwargs) -> str:
        """
        Convert the user document to a JSON string.

        This method sanitizes sensitive data and formats the MongoDB _id field as a string.

        Returns:
            JSON string representation of the user
        """
        data = self.to_mongo().to_dict()
        if "password" in data:
            del data["password"]

        if "_id" in data:
            data["id"] = str(data["_id"])
            del data["_id"]

        from json import dumps

        return dumps(data)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the user document to a Python dictionary.

        This method sanitizes sensitive data (removes password) and
        formats the MongoDB _id field as a string.

        Returns:
            Dictionary representation of the user
        """
        data = super().to_mongo().to_dict()
        if "password" in data:
            del data["password"]

        if "_id" in data:
            data["id"] = str(data["_id"])
            del data["_id"]

        return data
