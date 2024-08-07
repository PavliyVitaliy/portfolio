from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticDatabase
from odmantic import AIOEngine
from core.config import settings
from core.models.experience import Experience


class _MongoClientSingleton:
    mongo_client: AsyncIOMotorClient | None
    engine: AIOEngine

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(_MongoClientSingleton, cls).__new__(cls)
            cls.instance.mongo_client = AsyncIOMotorClient(settings.mongo.uri)
            cls.instance.engine = AIOEngine(
                client=cls.instance.mongo_client,
                database=settings.mongo.db,
            )
        return cls.instance


def mongo_database() -> AgnosticDatabase:
    return _MongoClientSingleton().mongo_client[settings.mongo.db]


def get_engine() -> AIOEngine:
    return _MongoClientSingleton().engine


async def mongo_database_ping():
    await mongo_database().command("ping")


async def mongo_configure_database():
    await get_engine().configure_database([Experience])
