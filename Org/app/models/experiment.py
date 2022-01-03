from typing import Any, Dict, Optional, List
from chaoslib.exceptions import ChaosException
from pydantic import BaseModel, validator, root_validator
from pydantic.error_wrappers import ValidationError
from pydantic.fields import Field
from datetime import datetime
from chaoslib.experiment import ensure_experiment_is_valid
from app.core.exception.exception_catalogue import ExceptionCatalogue

from app.core.exception.warg_exception import WargException




class ExperimentRequest(BaseModel):
    """
    Experiment Definition Model Request
    """

    experiment: Dict[Any, Any] = Field(
        ..., description="Chaos tooklit compatible Json file"
    )
    workspaceId: str = Field(..., description="id of parent workspace")

    @validator("experiment")
    def is_experimentJson_valid(cls, val):
        try:
            ensure_experiment_is_valid(val)
            return val
        except ChaosException as exc:
            raise WargException(
                status_code=422,
                error=ExceptionCatalogue.VALIDATION_ERROR,
                error_details=str(exc),
            )



class ExperimentResponse(BaseModel):
    """
    Experiment Model Response
    """

    experiment_name: str = Field(
        ..., description="Title of experiment from experiment payload"
    )
    experiment_description: str = Field(
        ...,
        description="Description of experiment from experiment payload",
    )
    experimentId: str = Field(..., description="Id of the experiment")
    workspaceId: str = Field(
        ..., description="Id of the workspace that the experiment belongs",
    )
    organizationId: str = Field(
        ...,
        description="Id of the organizaton that the experiment belongs",
    )
    creationTime: datetime = Field(
        ..., description="Creattion time of Experiment"
    )
    # lastModifiedTime: datetime = Field(
    #     ..., description="last modified time of Experiment"
    # )
    # version: str = Field(..., description="Version of the Experiment")

    class Config:
        extra = "ignore"
        allow_population_by_field_name = True


class ListExperiment(BaseModel):
    """
    Response model for API response of All Experiments
    """

    experiments: List[ExperimentResponse] = Field(
        default=[], description="LIst of all experiments"
    )

