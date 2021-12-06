from fastapi import APIRouter
from app.api.v1.endpoints import organization
from app.api.v1.endpoints import workspace

api_router: APIRouter = APIRouter()

api_router.include_router(
    organization.router, prefix="/organization", tags=["Organization"]
)
api_router.include_router(
    workspace.router, prefix="/workspace", tags=["Workspace"],
)

