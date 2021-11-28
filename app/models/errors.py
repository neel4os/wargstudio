from pydantic import BaseModel


class Error(BaseModel):
    error_code: str
    error_message: str
    error_deails: str = ""
