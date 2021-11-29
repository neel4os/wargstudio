from fastapi import APIRouter, Depends
from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorCollection
from starlette import responses
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


@router.get(
    "/{organizationId}",
    status_code=200,
    response_model=OrganizationRes,
    summary="Retrieve deails of a specific organization",
    description="Get details of organization defined by organizationId",
    response_model_by_alias=False,
)
async def get_organization(
    organizationId: str, collection: AsyncIOMotorCollection = Depends(get_db)
):
    response: OrganizationRes = await Organization(collection).read_specific(
        org_id=organizationId
    )
    return response
