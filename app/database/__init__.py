import os
from .session import sessionmanager
from .redis import RedisSingleton

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/contest_db")
MONGO_DB = os.getenv("MONGO_DB", "contest_db")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")


def init_db():
    sessionmanager.init(MONGO_URI, MONGO_DB)

    RedisSingleton.get_instance(REDIS_URL)


async def close_db():
    await sessionmanager.close()
    await RedisSingleton.delete_instance()
