from datetime import datetime
from typing import IO
from uuid import uuid4
from app.core.exception.exception_catalogue import ExceptionCatalogue

from app.core.exception.warg_exception import WargException
from app.models.experiment import ExperimentRequest, ExperimentResponse
from app.repositories.experiment_crud import ExperimentCrud
from app.service.workspace_service import Workspace
from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo.errors import PyMongoError


class Experiment:
    def __init__(self, dbConnection: AsyncIOMotorCollection) -> None:
        self._connection = dbConnection

    async def create(
        self, experiment_in: ExperimentRequest
    ) -> ExperimentResponse:
        try:
            _data = experiment_in.dict()
            _data["creationTime"] = datetime.utcnow()
            _data["lastModifiedTime"] = _data["creationTime"]
            _data["version"] = "1"
            _data["experimentId"] = str(uuid4()).replace("-", "")
            workspace_details = await Workspace(
                self._connection
            ).read_specific(_data["workspaceId"])
            await ExperimentCrud(
                self._connection,
                org_id=ObjectId(workspace_details.organizationId),
            ).create(_data)
            return ExperimentResponse(**_data)
        except PyMongoError as exc:
            raise WargException(
                status_code=503,
                error=ExceptionCatalogue.MONGO_DB_ERROR,
                error_details=str(exc),
            )
