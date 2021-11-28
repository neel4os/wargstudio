from fastapi import APIRouter, Depends
from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorCollection
from app.models.organization import OrganizationReq, OrganizationRes
from app.api.deps import get_db
from app.repositories.organization_crud import OrganizationCrud
from app.service.organization.organization_service import Organization

router: APIRouter = APIRouter()


@router.post(
    "/",
    status_code=201,
    response_model=OrganizationRes,
    summary="Create an Organization",
    description="Post request to create an organization",
)
async def create_organization(
    org_in: OrganizationReq, collection: AsyncIOMotorCollection = Depends(get_db)
):
    response: OrganizationRes = await Organization(collection).create(org_in)
    return response
