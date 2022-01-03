from typing import List, Optional
from pydantic import BaseModel
from pydantic.fields import Field

from app.models.scheduler import Scheduler


class JobReq(BaseModel):
    experimentId: str = Field(
        ..., description="id of experiment for the job"
    )
    scheduler: Optional[Scheduler] = Field(
        None, description="scheduler to run the experiment"
    )


class JobRes(JobReq):
    jobId: str = Field(..., description="id of the job")
    experimentId: str = Field(..., description="id of the parent experiment")
    workspaceId: str = Field(..., description="id of the parent workspace")
    organizationId: str = Field(..., description="id of the parent organization")


class ListJOb(BaseModel):
    jobs: List[JobRes] = Field(..., description="List of jobs")
