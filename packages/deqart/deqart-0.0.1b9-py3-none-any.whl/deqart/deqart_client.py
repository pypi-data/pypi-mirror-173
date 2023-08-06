from .api import jobs
from .backend_connection import BackendConnection
from .estimate_result import EstimateResult
from .job_result import JobResult


class DeqartClient:
    def __init__(self, api_token=None, config_location=None):
        self._backend_connection = BackendConnection(api_token, config_location)

    def search(self, run_status=None, created_later_than=None):
        """Search for jobs of the user
        :param run_status: if not None, run status of jobs to filter, can be one of "PENDING", "QUEUED", "RUNNING", "COMPLETED"
        :type run_status: str
        :param created_later_than: if not None, filter by latest datetime. Please add timezone for clarity, otherwise UTC will be assumed
        :type created_later_than: str or datetime.datetime
        :return: Metadata of jobs
        :rtype: list of JobResult
        """
        job_results = jobs.search_jobs(
            self._backend_connection, run_status, created_later_than
        )
        return [
            JobResult(dict(zip(job_results["column_names"], r)))
            for r in job_results["data"]
        ]

    def estimate(self, circuit):
        """Estimate job runtime
        :param circuit: Quantum circuit
        :type circuit: Cirq, Qiskit, circuit
        :return: Estimate result class
        :rtype: EstimateResult
        """
        return EstimateResult(
            jobs.estimate_job_runtime(self._backend_connection, circuit)
        )

    def run(self, circuit, asynchronous=False, debug_size=None):
        """Run job on Deqart Platform
        :param circuit: Quantum circuit
        :type circuit: Cirq, Qiskit, circuit
        :param asynchronous: if set to False, wait for job completion before returning. If set to True, return immediately
        :type asynchronous: bool
        :return: JobResult metadata
        :rtype: JobResult
        """
        submitted_job = jobs.submit_job(self._backend_connection, circuit, debug_size)
        if not asynchronous:
            return self.wait(submitted_job["job_id"])
        return JobResult(submitted_job)

    def wait(self, job_id):
        """Wait for job completion
        :param job_id: job_id that can be found as property of JobResult metadata
        :type job_id: str
        :return: JobResult metadata
        :rtype: JobResult
        """
        return JobResult(jobs.wait_for_job(self._backend_connection, job_id))
