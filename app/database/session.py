import motor.motor_asyncio
from mongoengine import connect, disconnect

mongo_client = None


class MongoDBSessionManager:
    def __init__(self):
        self._client = None
        self._db = None
        self._connected = False

    def init(self, uri: str, db_name: str):
        connect(db=db_name, host=uri)

        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self._db = self._client[db_name]
        self._connected = True

    async def close(self):
        if self._client:
            self._client.close()
            self._client = None
            self._db = None

        disconnect()
        self._connected = False

    @property
    def client(self):
        if not self._connected:
            raise Exception("MongoDBSessionManager is not initialized")

        return self._client

    @property
    def db(self):
        if not self._connected:
            raise Exception("MongoDBSessionManager is not initialized")

        return self._db

    @property
    def connected(self):
        return self._connected


sessionmanager = MongoDBSessionManager()


async def get_db():
    async def get_db_session():
        if not sessionmanager.connected:
            raise Exception("Database not connected")

        yield sessionmanager.db

    return get_db_session
