from rq.queue import Queue
from rq import Connection
from rq.job import Job
from app.models.job import JobReq
from app.repositories.minio_connection import MinioConnection
from app.repositories.minio_operation import MinioOperation
from app.repositories.worker import worker_function


class JobCrud:
    def __init__(self, queue: Queue) -> None:
        self._queue = queue

    def create_job(self, job_in: JobReq):
        MinioOperation(MinioConnection().create_connection()).get_object(
            job_in.experimentId,
            "definition/experiment",
            f"{job_in.experimentId}.json",
        )
        if not job_in.scheduler:
            return self._create_job_without_scheduler(job_in)

    def _create_job_without_scheduler(self, job_in):

        with Connection():
            job = Job.create(worker_function, [job_in])
            self._queue.enqueue_job(job)
            return job.id
