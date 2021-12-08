from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from app.repositories.base_crud import BaseCrud
from typing import Dict, Any
from pymongo import ReturnDocument


class WorkspaceCrud(BaseCrud):
    def __init__(
        self, collection: AsyncIOMotorCollection, org_id=None
    ) -> None:
        super().__init__(collection)
        self._org_id = org_id

    async def create(self, data: Dict[Any, Any]):
        return await self._collection.find_one_and_update(
            {"_id": self._org_id},
            {"$push": {"workspaces": data}},
            return_document=ReturnDocument.AFTER,
        )

    async def read_specific(self, data: Dict[Any, Any]):
        resource = await self._collection.find_one(
            {"workspaces": {"$elemMatch": data}}
        )

        return resource

    async def delete(self, ws_id):
        resource = await self.read_specific({"workspaceId": ws_id})
        if resource:
            await self._collection.update_one(
                {"_id": resource["_id"]},
                {"$pull": {"workspaces": {"workspaceId": ws_id}}},
            )
            return True
        return None

