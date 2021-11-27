from datetime import datetime
from typing import Any, Dict

from motor.motor_asyncio import AsyncIOMotorCollection
from app.models.organization import OrganizationReq, OrganizationRes
from app.repositories.organization_crud import OrganizationCrud


class Organization:
    def __init__(self, dboonnection : AsyncIOMotorCollection) -> None:
        self._collection = dboonnection

    async def create(self, org_in : OrganizationReq) -> OrganizationRes:
        _data = org_in.dict()
        _data["creation_time"] = datetime.utcnow()
        _data["last_modified_time"] = datetime.utcnow()
        _data["version"] = "1"
        _document = await OrganizationCrud(self._collection).create(data=_data)
        _data["organizationId"] = str(_document.inserted_id)
        return OrganizationRes(**_data)