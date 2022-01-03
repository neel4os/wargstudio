from fastapi.params import Depends
from app.api.deps import get_db
from app.models.job import JobReq, JobRes
from fastapi import APIRouter

from app.service.job_service import JobService

router: APIRouter = APIRouter()


@router.post(
    "/",
    status_code=201,
    response_model=JobRes,
    summary="Create an Job",
    description="Post request to create an job",
    response_model_exclude_none=True,
)
async def create_job(job_in: JobReq, queue=Depends(get_db)):
    return JobService(queue).create(job_in)



# @router.get(
#     "/{organizationId}",
#     status_code=200,
#     response_model=OrganizationRes,
#     summary="Retrieve deails of a specific organization",
#     description="Get details of organization defined by organizationId",
#     response_model_by_alias=False,
# )
# async def get_organization(
#     organizationId: str,
#     collection: AsyncIOMotorCollection = Depends(get_db),
# ):
#     response: OrganizationRes = await Organization(
#         collection
#     ).read_specific(org_id=organizationId)
#     return response


# @router.get(
#     "/",
#     status_code=200,
#     response_model=ListOrganization,
#     summary="Retrieve deails of organizations",
#     description="Get details of organizations",
#     response_model_by_alias=False,
# )
# async def get_organizations(
#     collection: AsyncIOMotorCollection = Depends(get_db),
# ):
#     response: ListOrganization = await Organization(collection).read()
#     return response


# @router.delete(
#     "/{organizationId}",
#     status_code=204,
#     summary="Delete an Organization",
#     description="Delete an organization defined by id",
# )
# async def delete_organization(
#     organizationId, collection: AsyncIOMotorCollection = Depends(get_db)
# ):
#     await Organization(collection).delete(organizationId)
#     return Response(status_code=204)


# @router.patch(
#     "/{organizationId}",
#     status_code=200,
#     summary="update an organization",
#     description="update an organization based on id",
# )
# async def update_orgnization(
#     org_in: OrganizationReq,
#     organizationId,
#     collection: AsyncIOMotorCollection = Depends(get_db),
# ):
#     resouces = await Organization(collection).update(
#         org_in, organizationId
#     )
#     return resouces
