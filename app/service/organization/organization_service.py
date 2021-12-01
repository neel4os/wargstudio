from datetime import datetime
from os import stat
from typing import Any, Dict, List
from pymongo.errors import PyMongoError
from motor.motor_asyncio import AsyncIOMotorCollection
from app.core.exception.exception_catalogue import ExceptionCatalogue
from app.core.exception.warg_exception import WargException
from app.models.errors import Error
from app.models.organization import OrganizationReq, OrganizationRes, ListOrganization
from app.repositories.organization_crud import OrganizationCrud
from bson.objectid import ObjectId


class Organization:
    def __init__(self, dboonnection: AsyncIOMotorCollection) -> None:
        self._collection = dboonnection

    async def create(self, org_in: OrganizationReq) -> OrganizationRes:
        try:
            _data = org_in.dict()
            _data["creationTime"] = datetime.utcnow()
            _data["lastModifiedTime"] = _data["creationTime"]
            _data["version"] = "1"
            _resource = await OrganizationCrud(self._collection).create(data=_data)
            _data["organizationId"] = str(_resource.inserted_id)
            _data.pop("_id")
            return OrganizationRes(**_data)
        except PyMongoError as exc:
            raise WargException(
                status_code=503,
                error=ExceptionCatalogue.MONGO_DB_ERROR,
                error_details=str(exc),
            )

    async def read_specific(self, org_id: str) -> OrganizationRes:
        try:
            _resource = await OrganizationCrud(self._collection).read_specific(
                data={"_id": ObjectId(org_id)}
            )
            if _resource:
                return OrganizationRes(**_resource)
            raise WargException(
                status_code=404,
                error=ExceptionCatalogue.NO_RESOURCE_ERROR,
                error_details=f"No Organization exists with id {org_id}",
            )
        except PyMongoError as exc:
            raise WargException(
                status_code=503,
                error=ExceptionCatalogue.MONGO_DB_ERROR,
                error_details=str(exc),
            )

    async def read(self) -> ListOrganization:
        try:
            _resources = await OrganizationCrud(self._collection).read_all()
            if _resources:
                return ListOrganization(
                    organizations=[
                        OrganizationRes(**_resource) for _resource in _resources
                    ]
                )
        except PyMongoError as exc:
            raise WargException(
                status_code=503,
                error=ExceptionCatalogue.MONGO_DB_ERROR,
                error_details=str(exc),
            )
