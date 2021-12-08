from app.api.deps import get_db
from app.models.organization import (
    ListOrganization,
    OrganizationReq,
    OrganizationRes,
)
from app.service.organization_service import Organization
from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorCollection

router: APIRouter = APIRouter()


@router.post(
    "/",
    status_code=201,
    response_model=OrganizationRes,
    summary="Create an Organization",
    description="Post request to create an organization",
    response_model_by_alias=False,
)
async def create_organization(
    org_in: OrganizationReq,
    collection: AsyncIOMotorCollection = Depends(get_db),
):
    response: OrganizationRes = await Organization(collection).create(
        org_in
    )
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
    organizationId: str,
    collection: AsyncIOMotorCollection = Depends(get_db),
):
    response: OrganizationRes = await Organization(
        collection
    ).read_specific(org_id=organizationId)
    return response


@router.get(
    "/",
    status_code=200,
    response_model=ListOrganization,
    summary="Retrieve deails of organizations",
    description="Get details of organizations",
    response_model_by_alias=False,
)
async def get_organizations(
    collection: AsyncIOMotorCollection = Depends(get_db),
):
    response: ListOrganization = await Organization(collection).read()
    return response


@router.delete(
    "/{organizationId}",
    status_code=204,
    summary="Delete an Organization",
    description="Delete an organization defined by id",
)
async def delete_organization(
    organizationId, collection: AsyncIOMotorCollection = Depends(get_db)
):
    resoures = await Organization(collection).delete(organizationId)
    return resoures


@router.patch(
    "/{organizationId}",
    status_code=200,
    summary="update an organization",
    description="update an organization based on id",
)
async def update_orgnization(
    org_in: OrganizationReq,
    organizationId,
    collection: AsyncIOMotorCollection = Depends(get_db),
):
    resouces = await Organization(collection).update(
        org_in, organizationId
    )
    return resouces
