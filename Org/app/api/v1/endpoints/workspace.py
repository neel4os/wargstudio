from app.api.deps import get_db
from app.models.workspace import (
    ListWorkspace,
    WorkspaceReq,
    WorkspaceRes,
)
from app.service.workspace_service import Workspace
from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorCollection

router: APIRouter = APIRouter()


@router.post(
    "/",
    status_code=201,
    response_model=WorkspaceRes,
    summary="Create an Workspace",
    description="Post request to create an workspace",
)
async def create_workspace(
    ws_in: WorkspaceReq,
    collection: AsyncIOMotorCollection = Depends(get_db),
):
    response: WorkspaceRes = await Workspace(collection).create(ws_in)
    return response


@router.get(
    "/{workspaceId}",
    status_code=200,
    response_model=WorkspaceRes,
    summary="Retrieve deails of a specific workspace",
    description="Get details of workspace defined by workspaceId",
    response_model_by_alias=False,
)
async def get_workspace(
    organizationID: str,
    workspaceId: str,
    collection: AsyncIOMotorCollection = Depends(get_db),
):
    response: WorkspaceRes = await Workspace(collection).read_specific(
        org_id=workspaceId
    )
    return response


@router.get(
    "/",
    status_code=200,
    response_model=ListWorkspace,
    summary="Retrieve deails of workspaces",
    description="Get details of workspaces",
    response_model_by_alias=False,
)
async def get_workspaces(
    collection: AsyncIOMotorCollection = Depends(get_db),
):
    response: ListWorkspace = await Workspace(collection).read()
    return response


@router.delete(
    "/{workspaceId}",
    status_code=204,
    summary="Delete an Workspace",
    description="Delete an workspace defined by id",
)
async def delete_workspace(
    workspaceId, collection: AsyncIOMotorCollection = Depends(get_db)
):
    resoures = await Workspace(collection).delete(workspaceId)
    return resoures


@router.patch(
    "/{workspaceId}",
    status_code=200,
    summary="update an workspace",
    description="update an workspace based on id",
)
async def update_orgnization(
    org_in: WorkspaceReq,
    workspaceId,
    collection: AsyncIOMotorCollection = Depends(get_db),
):
    resouces = await Workspace(collection).update(org_in, workspaceId)
    return resouces
