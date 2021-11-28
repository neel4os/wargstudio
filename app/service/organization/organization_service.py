from datetime import datetime
from typing import Any, Dict
from pymongo.errors import PyMongoError
from motor.motor_asyncio import AsyncIOMotorCollection
from app.core.exception.exception_catalogue import ExceptionCatalogue
from app.core.exception.warg_exception import WargException
from app.models.errors import Error
from app.models.organization import OrganizationReq, OrganizationRes
from app.repositories.organization_crud import OrganizationCrud


class Organization:
    def __init__(self, dboonnection: AsyncIOMotorCollection) -> None:
        self._collection = dboonnection

    async def create(self, org_in: OrganizationReq) -> OrganizationRes:
        try:
            _data = org_in.dict()
            _data["creation_time"] = datetime.utcnow()
            _data["last_modified_time"] = datetime.utcnow()
            _data["version"] = "1"
            _document = await OrganizationCrud(self._collection).create(data=_data)
            _data["organizationId"] = str(_document.inserted_id)
            return OrganizationRes(**_data)
        except PyMongoError as exc:
            raise WargException(
                status_code=503,
                error=ExceptionCatalogue.MONGO_DB_ERROR,
                error_deails=str(exc),
            )
