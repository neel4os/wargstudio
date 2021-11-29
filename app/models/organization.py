from typing import Optional
from pydantic import BaseModel
from pydantic.fields import Field
from datetime import datetime


class OrganizationReq(BaseModel):
    """
    Request model for Organization
    """

    name: Optional[str] = Field("", description="name of organisation")
    description: Optional[str] = Field("", description="description of organization")


class OrganizationRes(OrganizationReq):
    """
    Response model for the Organization
    """

    organizationId: str = Field(..., description="UUID of the Organization")
    creationTime: datetime = Field(..., description="Creattion time of Organization")
    lastModifiedTime: datetime = Field(
        ..., description="last modified time of Organization"
    )
    version: str = Field(..., description="Version of the Organization")

    class Config:
        extra = "ignore"

