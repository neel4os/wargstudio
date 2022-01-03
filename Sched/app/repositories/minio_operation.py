from minio import Minio
class MinioOperation:
    def __init__(self, connection) -> None:
        self._connection: Minio = connection

    def get_object(self, bucket_name, object_name, filepath):
        self._connection.fget_object(bucket_name, object_name, filepath)