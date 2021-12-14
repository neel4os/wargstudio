from app.api.deps import get_db
from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorCollection
from app.models.experiment import ExperimentRequest, ExperimentResponse
from app.service.experiment_service import Experiment

router: APIRouter = APIRouter()


@router.post(
    "/",
    status_code=201,
    response_model=ExperimentResponse,
    summary="Create an Experiment",
    description="Post request to create an Experiment",
)
async def create_experiment(
    experiment_in: ExperimentRequest,
    collection: AsyncIOMotorCollection = Depends(get_db),
):
    response: ExperimentResponse = await Experiment(collection).create(
        experiment_in
    )
    return response
