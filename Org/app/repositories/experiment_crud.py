from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo.collection import ReturnDocument
from app.repositories.base_crud import BaseCrud
from typing import Dict, Any, Optional

from app.repositories.workspace_crud import WorkspaceCrud


class ExperimentCrud(BaseCrud):
    def __init__(
        self,
        collection: AsyncIOMotorCollection,
        org_id: Optional[str] = None,
    ) -> None:
        super().__init__(collection)
        self._org_id = org_id

    async def create(self, data: Dict[Any, Any]):
        from devtools import debug

        debug(data["workspaceId"])
        return await self._collection.find_one_and_update(
            {"_id": self._org_id},
            {"$push": {"workspaces.$[workspace].experiments": data}},
            array_filters=[{"workspace.workspaceId": data["workspaceId"]}],
            return_document=ReturnDocument.AFTER
        )
