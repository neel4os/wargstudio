from typing import Any, Dict, Optional, List
from chaoslib.exceptions import ChaosException
from pydantic import BaseModel, validator, root_validator
from pydantic.error_wrappers import ValidationError
from pydantic.fields import Field
from datetime import datetime
from chaoslib.experiment import ensure_experiment_is_valid
from app.core.exception.exception_catalogue import ExceptionCatalogue

from app.core.exception.warg_exception import WargException


class ExperimentConfig(BaseModel):
    no_tls_verify: bool = Field(
        False, description="skip tls verification during validation"
    )

    class Config:
        extra = "forbid"


class ExperimentRequest(BaseModel):
    """
    Experiment Definition Model Request
    """

    experiment: Dict[Any, Any] = Field(
        ..., description="Chaos tooklit compatible Json file"
    )
    config: Optional[ExperimentConfig] = Field(
        ExperimentConfig(),
        description="configuration for verification of experimentJson",
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

    @root_validator(pre=True)
    def is_valid_config(cls, val):
        try:
            _config = val.get("config")
            if _config:
                print(" I am here and ", val.get("config"))
                ExperimentConfig(**val.get("config"))
                return val
            return val
        except ValidationError:
            raise WargException(
                status_code=422,
                error=ExceptionCatalogue.VALIDATION_ERROR,
                error_details="config can only be in format of {'no_tls_verify' : 'true'}",
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
        ..., description="UUID of the Workspace",
    )
    creationTime: datetime = Field(
        ..., description="Creattion time of Workspace"
    )
    lastModifiedTime: datetime = Field(
        ..., description="last modified time of Workspace"
    )
    version: str = Field(..., description="Version of the Workspace")

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

