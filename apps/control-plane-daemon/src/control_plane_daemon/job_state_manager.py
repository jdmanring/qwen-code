import os
import random
import time
from datetime import datetime
from typing import Any, cast

from .state_manager import StateManager


class JobStateManager:
    def __init__(self, settings_path: str | None = None) -> None:
        if settings_path is None:
            settings_path = os.path.expanduser("~/.qwen/settings.json")

        self.sm = StateManager()
        self.state_key = "active_job_set"

    def initialize_job_set(self, jobs: list[dict[str, Any]]) -> dict[str, Any]:
        """
        Initializes a new set of jobs for a task.
        """
        job_set = {
            "start_time": datetime.now().isoformat(),
            "jobs": {job["job_id"]: job for job in jobs},
        }
        self.sm.set(self.state_key, job_set)
        return job_set

    def update_job_status(self, job_id: str, status: str, result: Any = None) -> dict[str, Any]:
        """
        Updates the status of a specific job.
        Statuses: pending -> in_progress -> completed | failed | retrying | pivoting
        """
        job_set = self.sm.get(self.state_key)
        if not isinstance(job_set, dict) or job_id not in job_set["jobs"]:
            raise ValueError(f"Job {job_id} not found in active job set.")

        job = job_set["jobs"][job_id]
        job["status"] = status
        if result:
            job["result"] = result

        job["updated_at"] = datetime.now().isoformat()
        self.sm.set(self.state_key, job_set)
        return cast(dict[str, Any], job)

    def add_job(self, job: dict[str, Any]) -> dict[str, Any]:
        """
        Dynamically adds a new job to the active job set.
        """
        job_set = self.sm.get(self.state_key)
        if not isinstance(job_set, dict):
            raise ValueError("No active job set found. Initialize first.")

        job_id = job["job_id"]
        job_set["jobs"][job_id] = job
        self.sm.set(self.state_key, job_set)
        return job

    def get_next_job(self) -> dict[str, Any] | None:
        """
        Returns the first pending job whose dependencies are all completed.
        """
        job_set = self.sm.get(self.state_key)
        if not isinstance(job_set, dict):
            return None

        for _, job in job_set["jobs"].items():
            if job["status"] == "pending":
                # Check dependencies
                deps = job.get("dependencies", [])
                if all(job_set["jobs"].get(d, {}).get("status") == "completed" for d in deps):
                    return cast(dict[str, Any], job)

        return None

    def is_task_complete(self) -> bool:
        """
        Checks if all jobs in the set are completed.
        """
        job_set = self.sm.get(self.state_key)
        if not isinstance(job_set, dict):
            return True

        return all(job["status"] == "completed" for job in job_set["jobs"].values())

    def list_tasks(self) -> list[dict[str, Any]]:
        """Returns all jobs in the active set."""
        job_set = self.sm.get(self.state_key)
        if not isinstance(job_set, dict):
            return []
        return list(job_set["jobs"].values())

    def add_task(self, content: str) -> str:
        """Adds a simple task to the active set and returns its ID."""
        # Use timestamp + random suffix to avoid collisions in fast-execution loops
        job_id = f"task_{int(time.time())}_{random.randint(1000, 9999)}"
        job = {
            "job_id": job_id,
            "description": content,
            "status": "pending",
            "dependencies": [],
            "assigned_skill": "orchestrator",
            "job_type": "general",
            "verification_criteria": "Manual verification",
        }

        # Ensure a job set exists before adding
        if not self.sm.get(self.state_key):
            self.initialize_job_set([job])
            return job_id

        self.add_job(job)
        return job_id

    def complete_task(self, task_id: str) -> bool:
        """Marks a task as completed."""
        try:
            self.update_job_status(task_id, "completed")
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
        {"job_id": "j1", "status": "pending", "dependencies": []},
        {"job_id": "j2", "status": "pending", "dependencies": ["j1"]},
    ]
    jsm.initialize_job_set(jobs)
    next_job = jsm.get_next_job()
    if next_job:
        print(f"Next job: {next_job['job_id']}")  # Should be j1
    jsm.update_job_status("j1", "completed")
    next_job = jsm.get_next_job()
    if next_job:
        print(f"Next job: {next_job['job_id']}")  # Should be j2
