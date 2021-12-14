from typing import List, Optional
from pydantic import BaseModel
from pydantic.fields import Field
from datetime import datetime

from app.models.experiment import ExperimentResponse


class WorkspaceReq(BaseModel):
    """
    Request model for Workspace
    """

    name: Optional[str] = Field("", description="name of Workspace")
    description: Optional[str] = Field(
        "", description="description of Workspace"
    )
    organizationId: str = Field(
        ..., description="UUID of Parent Organization"
    )


class WorkspaceRes(WorkspaceReq):
    """
    Response model for the Workspace
    """

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


class ListWorkspace(BaseModel):
    """
    Response model for API response of All Workspace
    """

    workspaces: List[WorkspaceRes] = Field(
        ..., description="List of Workspaces"
    )


class WorkspaceModel(WorkspaceRes):
    experiments: List[ExperimentResponse] = Field(default=[])
