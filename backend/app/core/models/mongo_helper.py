from pymongo import ASCENDING, AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

from core.config import settings


class _MongoClientSingleton:
    mongo_client: AsyncMongoClient

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(_MongoClientSingleton, cls).__new__(cls)
            cls.instance.mongo_client = AsyncMongoClient(settings.mongo.uri)
        return cls.instance


def mongo_database() -> AsyncDatabase:
    return _MongoClientSingleton().mongo_client[settings.mongo.db]


async def mongo_database_ping():
    await mongo_database().command("ping")


async def mongo_configure_database():
    await mongo_database().experience.create_index(
        [("user_id", ASCENDING)],
        unique=True,
    )


def mongo_close() -> None:
    _MongoClientSingleton().mongo_client.close()
