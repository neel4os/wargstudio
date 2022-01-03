from typing import Literal, Optional
from pydantic import BaseModel, validator
from app.core.util.time_helper import SchedTime


class Scheduler(BaseModel):
    type: Literal["once", "repeat"]
    execute: str
    condition: Optional[str]
    prob: Optional[float]

    @validator("condition")
    def condition_not_be_present_when_type_once(cls, v, values):
        if values["type"] == "once" and v:
            raise ValueError(
                "for type once condition shall not be present"
            )

    @validator("prob")
    def prob_not_be_presrnt_when_type_once(cls, v, values):
        if values["type"] == "once" and v:
            raise ValueError("for type once prob shall not be present")

    @validator("execute")
    def convert_execute(cls, v, values):
        try:
            return SchedTime().parse_execute(values["type"], v)
        except:
            raise ValueError(f"{v} can not be parsed")

