import io
import json

from app.core.exception.exception_catalogue import ExceptionCatalogue
from app.core.exception.warg_exception import WargException
from app.core.util.error_decorator import MinioErrorHandler
from app.repositories.minio_connection import MinioConnection
from minio.api import Minio
from minio.commonconfig import Tags


class MinioOperation:
    def __init__(self) -> None:
        self._client: Minio = MinioConnection().create_connection()

    def upload_experiment(self, _data):
        bucket_name = _data["experimentId"]
        experiment = _data["experiment"]
        self.create_bucket(bucket_name)
        self.put_tags_in_bucket(bucket_name, _data)
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
    def put_tags_in_bucket(self, bucket_name, _data):
        tags = Tags.new_bucket_tags()
        tags["organizationId"] = _data["organizationId"]
        tags["workspaceId"] = _data["workspaceId"]
        self._client.set_bucket_tags(bucket_name, tags)

    @MinioErrorHandler
    def put_experiment_file(self, bucket_name, experiment):
        self._client.put_object(
            bucket_name=bucket_name,
            object_name=f"definition/experiment",
            data=io.BytesIO(json.dumps(experiment).encode("utf-8")),
            length=-1,
            part_size=10 * 1024 * 1024,
        )

    @MinioErrorHandler
    def get_all_object_bucket(self, bucket_name):
        self._objects = self._client.list_objects(
            bucket_name, prefix="definition", recursive=True
        )

    @MinioErrorHandler
    def delete_bucket(self, bucket_name):
        self.get_all_object_bucket(bucket_name)
        for obj in self._objects:
            self._client.remove_object(bucket_name, obj.object_name)
        self._client.remove_bucket(bucket_name)
