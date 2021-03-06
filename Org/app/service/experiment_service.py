from datetime import datetime
from uuid import uuid4
from app.core.exception.exception_catalogue import ExceptionCatalogue
from app.core.exception.warg_exception import WargException
from app.core.util.error_decorator import MongoErrorHandler
from app.models.experiment import (
    ExperimentRequest,
    ExperimentResponse,
    ListExperiment,
)
from app.models.workspace import WorkspaceRes
from app.repositories.experiment_crud import ExperimentCrud
from app.repositories.minio_operation import MinioOperation
from app.service.workspace_service import Workspace
from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from app.repositories.organization_crud import OrganizationCrud


class Experiment:
    def __init__(self, dbConnection: AsyncIOMotorCollection) -> None:
        self._connection = dbConnection

    @MongoErrorHandler
    async def create(
        self, experiment_in: ExperimentRequest
    ) -> ExperimentResponse:
        _ws_details: WorkspaceRes = await Workspace(
            self._connection
        ).read_specific(experiment_in.workspaceId)
        _data = experiment_in.dict()
        _data["creationTime"] = datetime.utcnow()
        # _data["lastModifiedTime"] = _data["creationTime"]
        # _data["version"] = "1"
        _data["experimentId"] = str(uuid4()).replace("-", "")
        _data["experiment_name"] = _data["experiment"]["title"]
        _data["experiment_description"] = _data["experiment"][
            "description"
        ]
        _data["organizationId"] = _ws_details.organizationId
        workspace_details = await Workspace(
            self._connection
        ).read_specific(_data["workspaceId"])
        await ExperimentCrud(
            self._connection,
            org_id=ObjectId(workspace_details.organizationId),
        ).create(_data)
        MinioOperation().upload_experiment(
            _data
        )
        return ExperimentResponse(**_data)

    @MongoErrorHandler
    async def read(self) -> ListExperiment:
        _resources = await OrganizationCrud(self._connection).read_all()
        _experiment_resource = []
        if _resources:
            for org in _resources:
                for ws in org["workspaces"]:
                    _experiment_resource = (
                        _experiment_resource + ws["experiments"]
                    )
            return ListExperiment(
                experiments=[
                    ExperimentResponse(**res)
                    for res in _experiment_resource
                ]
            )
        else:
            return ListExperiment()

    @MongoErrorHandler
    async def read_specific(self, experimentId: str) -> ExperimentResponse:
        _response = await self.read()
        list_experiments = _response.experiments
        if list_experiments:
            try:
                _exp_resp = [
                    _resp
                    for _resp in list_experiments
                    if _resp.experimentId == experimentId
                ][0]
                return _exp_resp
            except IndexError:
                raise WargException(
                    status_code=404,
                    error=ExceptionCatalogue.NO_RESOURCE_ERROR,
                    error_details=f"No Experiment exists with id {experimentId}",
                )

        raise WargException(
            status_code=404,
            error=ExceptionCatalogue.NO_RESOURCE_ERROR,
            error_details=f"No Experiment exists with id {experimentId}",
        )

    @MongoErrorHandler
    async def delete(self, experimentId) -> None:
        exp_details: ExperimentResponse = await self.read_specific(
            experimentId
        )
        await ExperimentCrud(self._connection).delete(exp_details)
        MinioOperation().delete_bucket(experimentId)

