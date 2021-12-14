from minio.api import Minio
from app.core.exception.exception_catalogue import ExceptionCatalogue
from app.core.util.error_decorator import MinioErrorHandler
from app.repositories.minio_connection import MinioConnection
from app.core.exception.warg_exception import WargException
import json
import io


class MinioOperation:
    def __init__(self) -> None:
        self._client: Minio = MinioConnection().create_connection()

    def upload_experiment(self, bucket_name, experiment):
        self.create_bucket(bucket_name)
        self.put_experiment_file(bucket_name, experiment)

    @MinioErrorHandler
    def create_bucket(self, bucket_name):
        if self._client.bucket_exists(bucket_name):
            raise WargException(
                status_code=503,
                error=ExceptionCatalogue.STORAGE_ERROR,
                error_details=f"bucket exist with name {bucket_name}",
            )
        self._client.make_bucket(bucket_name)

    @MinioErrorHandler
    def put_experiment_file(self, bucket_name, experiment):
        self._client.put_object(
            bucket_name=bucket_name,
            object_name=f"definition/experiment",
            data=io.BytesIO(json.dumps(experiment).encode("utf-8")),
            length=-1,
            part_size=10 * 1024 * 1024,
        )

