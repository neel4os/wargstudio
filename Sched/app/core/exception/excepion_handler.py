from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.exception.exception_catalogue import ExceptionCatalogue
from app.core.exception.sched_exception import SchedException
from app.models.errors import Error
import traceback


async def global_exception_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        print(traceback.format_exc(), sep="\n")
        return JSONResponse(
            status_code=500,
            content=Error(
                error_code=ExceptionCatalogue.DEFAULT_ERROR.error_code,
                error_message=str(e),
            ).dict(),
        )


async def sched_exception_handler(request: Request, exc: SchedException):
    return JSONResponse(
        status_code=exc._status_code, content=exc._model.dict(),
    )
