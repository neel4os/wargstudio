from rq import job
from rq.job import Job
from rq.queue import Queue
from rq import Connection
from app.core.exception.exception_catalogue import ExceptionCatalogue
from app.core.exception.sched_exception import SchedException
from app.models.job import JobReq, JobRes
from app.repositories.job_crud import JobCrud
from datetime import datetime
from minio import Minio

from app.repositories.minio_connection import MinioConnection


class JobService:
    def __init__(self, queue: Queue) -> None:
        self._queue = queue

    def create(self, job_in: JobReq):
        _conn: Minio = MinioConnection().create_connection()
        if _conn.bucket_exists(job_in.experimentId):
            tags = _conn.get_bucket_tags(job_in.experimentId)
            job_id = JobCrud(self._queue).create_job(job_in)
            _data = job_in.dict()
            _data["jobId"] = job_id
            _data.update(tags)
            return JobRes(**_data)
        else:
            raise SchedException(
                status_code=503,
                error=ExceptionCatalogue.STORAGE_ERROR,
                error_details=f"No experiment registered with id {job_in.experimentId}",
            )



