from typing import Generic, Type, TypeVar

from mongoengine import Document, EmailField, QuerySet, StringField

U = TypeVar("U", bound=Document)


class QuerySetManager(Generic[U]):
    def __get__(self, instance: object, cls: Type[U]) -> QuerySet:
        return QuerySet(cls, cls._get_collection())


class User(Document):
    meta = {"collection": "users"}

    name = StringField(required=True, max_length=30)
    email = EmailField(required=True, unique=True)

    objects = QuerySetManager["User"]()
