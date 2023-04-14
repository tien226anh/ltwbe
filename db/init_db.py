from motor.motor_asyncio import AsyncIOMotorClient

from core.config import settings

db_client = AsyncIOMotorClient(settings.MONGO_DETAILS)
database = db_client[settings.DATABASE_NAME]


async def connect_db():
    """Create database connection."""
    global db_client
    db_client = AsyncIOMotorClient(settings.MONGO_DETAILS)


async def close_db():
    """Close database connection."""
    db_client.close()


def get_collection_client(table: str):
    return database.get_collection(table)
