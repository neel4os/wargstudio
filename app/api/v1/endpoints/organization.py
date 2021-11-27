from fastapi import APIRouter, Depends
from datetime import datetime
from app.models.organization import OrganizationReq, OrganizationRes
from app.api.deps import get_db
from app.repositories.organization_crud import OrganizationCrud

router: APIRouter = APIRouter()


@router.post(
    "/",
    status_code=201,
    response_model=OrganizationRes,
    summary="Create an Organization",
    description="Post request to create an organization",
)
async def create_organization(org_in: OrganizationReq, collection=Depends(get_db)):
    _data = org_in.dict()
    _data["creation_time"] = datetime.utcnow()
    _data["last_modified_time"] = datetime.utcnow()
    _data["version"] = "1"
    _document = await OrganizationCrud(collection).create(data=_data)
    _data["organizationId"] = str(_document.inserted_id)
    raise IOError
    return OrganizationRes(**_data)
