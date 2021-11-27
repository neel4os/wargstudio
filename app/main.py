from fastapi import FastAPI
from app.core.config.settings import _setting
from app.api.v1.api import api_router

app: FastAPI = FastAPI(title=_setting.title, description=_setting.description)

app.include_router(api_router)