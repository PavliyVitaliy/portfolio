from os import getenv
from urllib.parse import urlsplit, urlunsplit

from pymongo import ASCENDING, AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

from core.config import settings


class _MongoClientSingleton:
    mongo_client: AsyncMongoClient

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(_MongoClientSingleton, cls).__new__(cls)
            cls.instance.mongo_client = AsyncMongoClient(_mongo_uri())
        return cls.instance


def _mongo_uri() -> str:
    authority_override = getenv("MONGO_URI_AUTHORITY_OVERRIDE")
    if authority_override is None:
        return settings.mongo.uri

    uri = urlsplit(settings.mongo.uri)
    user_info, separator, _ = uri.netloc.rpartition("@")
    netloc = f"{user_info}@{authority_override}" if separator else authority_override
    return urlunsplit(uri._replace(netloc=netloc))


def mongo_database() -> AsyncDatabase:
    return _MongoClientSingleton().mongo_client[settings.mongo.db]


async def mongo_database_ping():
    await mongo_database().command("ping")


async def mongo_configure_database():
    await mongo_database().experience.create_index(
        [("user_id", ASCENDING)],
        unique=True,
    )
    await mongo_database().profile.create_index(
        [("user_id", ASCENDING)],
        unique=True,
    )
    await mongo_database().projects.create_index(
        [("user_id", ASCENDING), ("sort_order", ASCENDING)],
    )


async def mongo_close() -> None:
    if hasattr(_MongoClientSingleton, "instance"):
        await _MongoClientSingleton.instance.mongo_client.close()
        del _MongoClientSingleton.instance
