from abc import ABC
from typing import Any, Dict
from motor.motor_asyncio import AsyncIOMotorCollection

class BaseCrud(ABC):
    def __init__(self, collection: AsyncIOMotorCollection) -> None:
        self._collection: AsyncIOMotorCollection = collection

    async def create(self, data: Dict[Any,Any]):
        return await self._collection.insert_one(data)