from abc import ABC
from typing import Any, Dict
from motor.motor_asyncio import AsyncIOMotorCollection
from bson import json_util
import json

from app.core.util.mongo_json_serializer import MongoDbOrganizaionEncoder


class BaseCrud(ABC):
    def __init__(self, collection: AsyncIOMotorCollection) -> None:
        self._collection: AsyncIOMotorCollection = collection

    async def create(self, data: Dict[Any, Any]):
        return await self._collection.insert_one(data)

    async def read_specific(self, data):
        resource = await self._collection.find_one(data)
        if resource:
            return json.loads(json.dumps(resource, cls=MongoDbOrganizaionEncoder))

