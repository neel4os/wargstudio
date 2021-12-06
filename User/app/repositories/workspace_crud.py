from motor.motor_asyncio import AsyncIOMotorCollection
from app.repositories.base_crud import BaseCrud
from typing import Dict, Any
from pymongo import ReturnDocument


class WorkspaceCrud(BaseCrud):
    def __init__(
        self, collection: AsyncIOMotorCollection, org_id: str
    ) -> None:
        super().__init__(collection)
        self._org_id = org_id

    async def create(self, data: Dict[Any, Any]):
        return await self._collection.find_one_and_update(
            {"_id": self._org_id},
            {"$push": {"workspaces": data}},
            return_document=ReturnDocument.AFTER,
        )

