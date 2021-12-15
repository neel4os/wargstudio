from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo.collection import ReturnDocument
from app.models.experiment import ExperimentResponse
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
        return await self._collection.find_one_and_update(
            {"_id": self._org_id},
            {"$push": {"workspaces.$[workspace].experiments": data}},
            array_filters=[{"workspace.workspaceId": data["workspaceId"]}],
            return_document=ReturnDocument.AFTER,
        )

    async def delete(self, exp_details: ExperimentResponse):
        from devtools import debug

        debug(exp_details.experimentId)
        await self._collection.update_one(
            {"_id": ObjectId(exp_details.organizationId)},
            {
                "$pull": {
                    "workspaces.$[].experiments": {
                        "experimentId": exp_details.experimentId
                    }
                }
            },
        )
        return True
