from chaoslib.experiment import run_experiment
import json

from app.models.job import JobReq


def worker_function(job_in: JobReq):
    Worker(job_in).do_work()


class Worker:
    def __init__(self, job_in: JobReq) -> None:
        self.job_in: JobReq = job_in

    def do_work(self):
        print(self.job_in)
        # self.fetch_experiment()
        # self.create_object_in_bucket()
        self.run_chaostk()
        # self.upload_result()

    def run_chaostk(self):
        with open(f"{self.job_in.experimentId}.json") as _file:
            experiment_dict = json.load(_file)
        p = run_experiment(experiment_dict)
        from devtools import debug

        print(p)

