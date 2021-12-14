from functools import wraps
from pymongo.errors import PyMongoError

from app.core.exception.exception_catalogue import ExceptionCatalogue
from app.core.exception.warg_exception import WargException


def MongoErrorHandler(func):
    @wraps(func)
    async def wrapped(self, *args, **kwargs):
        try:
            return await func(self, *args, **kwargs)
        except PyMongoError as exc:
            raise WargException(
                status_code=503,
                error=ExceptionCatalogue.MONGO_DB_ERROR,
                error_details=str(exc),
            )

    return wrapped


def MinioErrorHandler(func):
    @wraps(func)
    def wrapped(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as exc:
            raise WargException(
                status_code=503,
                error=ExceptionCatalogue.STORAGE_ERROR,
                error_details=str(exc),
            )

    return wrapped