from fastapi import APIRouter
from app.api.v1.endpoints import organization
from app.api.v1.endpoints import workspace
from app.api.v1.endpoints import experiment

api_router: APIRouter = APIRouter()

api_router.include_router(
    organization.router, prefix="/organization", tags=["Organization"]
)
api_router.include_router(
    workspace.router, prefix="/workspace", tags=["Workspace"],
)

api_router.include_router(
    experiment.router, prefix="/experiment", tags=["experiment"]
)

