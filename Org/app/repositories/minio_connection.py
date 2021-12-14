from minio.error import MinioException
from app.core.config.settings import _setting
from app.core.exception.exception_catalogue import ExceptionCatalogue
from app.core.util.singleton import Singleton
from minio import Minio
from app.core.exception.warg_exception import WargException


class MinioConnection(metaclass=Singleton):
    def __init__(self) -> None:
        self._endpoint: str = _setting.MinioUrl
        self._access_key: str = _setting.MinioAcessKey
        self._secret_key: str = _setting.MinioSecretKry

    def create_connection(self):
        try:
            return Minio(
                self._endpoint,
                self._access_key,
                self._secret_key,
                secure=False,
            )
        except MinioException as exc:
            raise WargException(
                status_code=503,
                error=ExceptionCatalogue.STORAGE_ERROR,
                error_details=str(exc),
            )

