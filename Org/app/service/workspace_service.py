from datetime import datetime
from uuid import uuid4

from app.core.exception.exception_catalogue import ExceptionCatalogue
from app.core.exception.warg_exception import WargException
from app.models.workspace import ListWorkspace, WorkspaceReq, WorkspaceRes
from app.repositories.organization_crud import OrganizationCrud
from app.repositories.workspace_crud import WorkspaceCrud
from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo.errors import PyMongoError


class Workspace:
    def __init__(self, dboonnection: AsyncIOMotorCollection) -> None:
        self._collection = dboonnection

    async def create(self, ws_in: WorkspaceReq) -> WorkspaceRes:
        try:
            _data = ws_in.dict()
            _data["creationTime"] = datetime.utcnow()
            _data["lastModifiedTime"] = _data["creationTime"]
            _data["version"] = "1"
            _data["workspaceId"] = str(uuid4()).replace("-", "")
            _data["experiments"] = []
            _resource = await WorkspaceCrud(
                self._collection, org_id=ObjectId(_data["organizationId"])
            ).create(data=_data)
            _return_data = [
                elem
                for elem in _resource["workspaces"]
                if elem["workspaceId"] == _data["workspaceId"]
            ][0]
            return WorkspaceRes(**_return_data)
        except PyMongoError as exc:
            raise WargException(
                status_code=503,
                error=ExceptionCatalogue.MONGO_DB_ERROR,
                error_details=str(exc),
            )

    async def read_specific(self, ws_id: str) -> WorkspaceRes:
        try:
            _resource = await WorkspaceCrud(
                self._collection
            ).read_specific(data={"workspaceId": ws_id})
            if _resource:
                _return_data = [
                    elem
                    for elem in _resource["workspaces"]
                    if elem["workspaceId"] == ws_id
                ][0]
                return WorkspaceRes(**_return_data)
            raise WargException(
                status_code=404,
                error=ExceptionCatalogue.NO_RESOURCE_ERROR,
                error_details=f"No Workspace exists with id {ws_id}",
            )
        except PyMongoError as exc:
            raise WargException(
                status_code=503,
                error=ExceptionCatalogue.MONGO_DB_ERROR,
                error_details=str(exc),
            )

    async def read(self) -> ListWorkspace:
        try:
            _resources = await OrganizationCrud(
                self._collection
            ).read_all()
            _workspace_resource = []
            if _resources:
                for org in _resources:
                    _workspace_resource = (
                        _workspace_resource + org["workspaces"]
                    )
                return ListWorkspace(
                    workspaces=[
                        WorkspaceRes(**res) for res in _workspace_resource
                    ]
                )
        except PyMongoError as exc:
            raise WargException(
                status_code=503,
                error=ExceptionCatalogue.MONGO_DB_ERROR,
                error_details=str(exc),
            )

    async def delete(self, ws_id) -> None:
        try:
            _resources = await WorkspaceCrud(self._collection).delete(
                ws_id
            )
            if not _resources:
                raise WargException(
                    status_code=404,
                    error=ExceptionCatalogue.NO_RESOURCE_ERROR,
                    error_details=f"No Workspace exists with id {ws_id}",
                )
        except PyMongoError as exc:
            raise WargException(
                status_code=503,
                error=ExceptionCatalogue.MONGO_DB_ERROR,
                error_details=str(exc),
            )

    async def update(self, ws_in, ws_id) -> WorkspaceRes:
        try:
            _resource = await self.read_specific(ws_id)
            _data = ws_in.dict(exclude_defaults=True)
            _data["version"] = str(int(_resource.version) + 1)
            _data["lastModifiedTime"] = datetime.utcnow()
            await WorkspaceCrud(self._collection).update(
                filter_cond={"_id": ObjectId(ws_id)}, data=_data
            )
            return await self.read_specific(ws_id)
        except PyMongoError as exc:
            raise WargException(
                status_code=503,
                error=ExceptionCatalogue.MONGO_DB_ERROR,
                error_details=str(exc),
            )
