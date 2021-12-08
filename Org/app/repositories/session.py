from app.core.config.settings import _setting
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorDatabase,
)

from app.core.util.singleton import Singleton


class DbSession(metaclass=Singleton):
    def __init__(self) -> None:
        self._db_url: str = _setting.DbURL
        self._client: AsyncIOMotorClient = AsyncIOMotorClient(self._db_url)
        self._database: AsyncIOMotorDatabase = self._client[
            _setting.Database_name
        ]
        self._collection: AsyncIOMotorCollection = self._database[
            _setting.Collection_name
        ]

    @property
    def client(self):
        return self._client

    @property
    def database(self):
        return self._database

    @property
    def collection(self):
        return self._collection
