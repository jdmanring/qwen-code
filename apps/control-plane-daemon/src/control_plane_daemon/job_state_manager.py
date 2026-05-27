import os
import random
import time
from datetime import datetime
from typing import Any

from .models import Job, JobSet, JobStatus, JobType
from .state_manager import StateManager


class JobStateManager:
    def __init__(self, settings_path: str | None = None) -> None:
        if settings_path is None:
            settings_path = os.path.expanduser("~/.qwen/settings.json")

        self.sm = StateManager()
        self.state_key = "active_job_set"

    def _get_job_set(self) -> JobSet | None:
        """Helper to retrieve and validate the current job set."""
        data = self.sm.get(self.state_key)
        if not data:
            return None
        try:
            return JobSet(**data)
        except (TypeError, ValueError):
            return None

    def initialize_job_set(self, jobs_data: list[dict[str, Any]]) -> JobSet:
        """
        Initializes a new set of jobs for a task.
        """
        jobs = {data["job_id"]: Job(**data) for data in jobs_data}

        job_set = JobSet(start_time=datetime.now().isoformat(), jobs=jobs)

        self.sm.set(self.state_key, job_set.model_dump())
        return job_set

    def update_job_status(self, job_id: str, status: JobStatus, result: Any = None) -> Job:
        """
        Updates the status of a specific job.
        """
        job_set = self._get_job_set()
        if not job_set or job_id not in job_set.jobs:
            raise ValueError(f"Job {job_id} not found in active job set.")

        job = job_set.jobs[job_id]
        job.status = status
        if result:
            job.result = result

        job.updated_at = datetime.now().isoformat()

        self.sm.set(self.state_key, job_set.model_dump())
        return job

    def add_job(self, job: Job) -> Job:
        """
        Dynamically adds a new job to the active job set.
        """
        job_set = self._get_job_set()
        if not job_set:
            raise ValueError("No active job set found. Initialize first.")

        job_set.jobs[job.job_id] = job
        self.sm.set(self.state_key, job_set.model_dump())
        return job

    def get_next_job(self) -> Job | None:
        """
        Returns the first pending job whose dependencies are all completed.
        """
        job_set = self._get_job_set()
        if not job_set:
            return None

        for job in job_set.jobs.values():
            if job.status == JobStatus.PENDING:
                # Check dependencies
                if all(
                    job_set.jobs.get(d) and job_set.jobs[d].status == JobStatus.COMPLETED
                    for d in job.dependencies
                ):
                    return job

        return None

    def is_task_complete(self) -> bool:
        """
        Checks if all jobs in the set are completed.
        """
        job_set = self._get_job_set()
        if not job_set:
            return True

        return all(job.status == JobStatus.COMPLETED for job in job_set.jobs.values())

    def list_tasks(self) -> list[Job]:
        """Returns all jobs in the active set."""
        job_set = self._get_job_set()
        if not job_set:
            return []
        return list(job_set.jobs.values())

    def add_task(self, content: str) -> str:
        """Adds a simple task to the active set and returns its ID."""
        job_id = f"task_{int(time.time())}_{random.randint(1000, 9999)}"
        job = Job(
            job_id=job_id,
            description=content,
            status=JobStatus.PENDING,
            dependencies=[],
            assigned_skill="orchestrator",
            job_type=JobType.GENERAL,
            verification_criteria="Manual verification",
        )

        if not self._get_job_set():
            self.initialize_job_set([job.model_dump()])
            return job_id

        self.add_job(job)
        return job_id

    def complete_task(self, task_id: str) -> bool:
        """Marks a task as completed."""
        try:
            self.update_job_status(task_id, JobStatus.COMPLETED)
            return True
        except ValueError:
            return False

    def clear_jobs(self) -> None:
        """
        Clears the active job set.
        """
        self.sm.delete(self.state_key)


if __name__ == "__main__":
    jsm = JobStateManager()
    # Mock jobs
    jobs = [
        {"job_id": "j1", "status": JobStatus.PENDING, "dependencies": []},
        {"job_id": "j2", "status": JobStatus.PENDING, "dependencies": ["j1"]},
    ]
    jsm.initialize_job_set(jobs)
    next_job = jsm.get_next_job()
    if next_job:
        print(f"Next job: {next_job.job_id}")  # Should be j1
    jsm.update_job_status("j1", JobStatus.COMPLETED)
    next_job = jsm.get_next_job()
    if next_job:
        print(f"Next job: {next_job.job_id}")  # Should be j2
