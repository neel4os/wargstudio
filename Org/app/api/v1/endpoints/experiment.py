from app.api.deps import get_db
from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorCollection
from app.models.experiment import (
    ExperimentRequest,
    ExperimentResponse,
    ListExperiment,
)
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


@router.get(
    "/",
    status_code=200,
    response_model=ListExperiment,
    summary="Retrieve deails of experiments",
    description="Get details of experiments",
    response_model_by_alias=False,
)
async def get_experiments(
    collection: AsyncIOMotorCollection = Depends(get_db),
):
    response: ListExperiment = await Experiment(collection).read()
    return response


@router.get(
    "/{experimentId}",
    status_code=200,
    response_model=ExperimentResponse,
    summary="Retrieve deails of specific experiment",
    description="Get details of specific experiment",
    response_model_by_alias=False,
)
async def get_experiments(
    experimentId: str,
    collection: AsyncIOMotorCollection = Depends(get_db),
):
    response: ExperimentResponse = await Experiment(
        collection
    ).read_specific(experimentId=experimentId)
    return response
