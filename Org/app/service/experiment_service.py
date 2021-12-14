from datetime import datetime
from uuid import uuid4
from app.core.util.error_decorator import MongoErrorHandler
from app.models.experiment import ExperimentRequest, ExperimentResponse
from app.repositories.experiment_crud import ExperimentCrud
from app.repositories.minio_operation import MinioOperation
from app.service.workspace_service import Workspace
from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection


class Experiment:
    def __init__(self, dbConnection: AsyncIOMotorCollection) -> None:
        self._connection = dbConnection

    @MongoErrorHandler
    async def create(
        self, experiment_in: ExperimentRequest
    ) -> ExperimentResponse:
        _data = experiment_in.dict()
        _data["creationTime"] = datetime.utcnow()
        _data["lastModifiedTime"] = _data["creationTime"]
        _data["version"] = "1"
        _data["experimentId"] = str(uuid4()).replace("-", "")
        _data["experiment_name"] = _data["experiment"]["title"]
        _data["experiment_description"] = _data["experiment"][
            "description"
        ]
        workspace_details = await Workspace(
            self._connection
        ).read_specific(_data["workspaceId"])
        await ExperimentCrud(
            self._connection,
            org_id=ObjectId(workspace_details.organizationId),
        ).create(_data)
        MinioOperation().upload_experiment(
            _data["experimentId"], _data["experiment"]
        )
        return ExperimentResponse(**_data)
