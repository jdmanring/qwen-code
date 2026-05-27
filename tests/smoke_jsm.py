from control_plane_daemon.job_state_manager import JobStateManager
from control_plane_daemon.models import JobStatus


def test_jsm():
    jsm = JobStateManager()
    jsm.clear_jobs()

    print("Testing add_task...")
    tid = jsm.add_task("Test task 1")
    print(f"Added task: {tid}")

    print("Testing get_next_job...")
    job = jsm.get_next_job()
    print(f"Next job: {job.job_id if job else 'None'}")

    print("Testing update_job_status...")
    jsm.update_job_status(tid, JobStatus.COMPLETED)

    print("Testing is_task_complete...")
    print(f"Complete: {jsm.is_task_complete()}")


if __name__ == "__main__":
    test_jsm()
