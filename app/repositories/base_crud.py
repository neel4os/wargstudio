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

    async def read_specific(self, data: Dict[Any, Any]):
        resource = await self._collection.find_one(data)
        if resource:
            return json.loads(json.dumps(resource, cls=MongoDbOrganizaionEncoder))

    async def read_all(self):
        resources = []
        async for resource in self._collection.find():
            resources.append(
                json.loads(json.dumps(resource, cls=MongoDbOrganizaionEncoder))
            )
        return resources

    async def delete(self, data: Dict[Any, Any]):
        resource = await self.read_specific(data=data)
        if resource:
            await self._collection.delete_one(data)
            return True

    async def update(self, filter_cond, field, value):
        resource = await self._collection.update_one(
            filter_cond, {"$push": {field: value}}
        )
        if resource:
            return resource
