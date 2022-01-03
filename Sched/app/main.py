from fastapi import FastAPI
from app.core.config.settings import _setting
from app.api.v1.api import api_router
from app.core.exception.excepion_handler import (
    global_exception_middleware,
    sched_exception_handler,
)
from app.core.exception.sched_exception import SchedException


app: FastAPI = FastAPI(
    title=_setting.title, description=_setting.description
)

app.include_router(api_router)
app.middleware("http")(global_exception_middleware)
app.exception_handler(SchedException)(sched_exception_handler)
