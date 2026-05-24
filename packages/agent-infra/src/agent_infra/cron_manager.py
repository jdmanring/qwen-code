import os
import subprocess


class CronManager:
    def __init__(self) -> None:
        self.user = os.environ.get("USER")

    def list_jobs(self) -> str:
        """Lists all current crontabs for the user."""
        try:
            result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            if "no crontab for" in e.stderr:
                return ""
            raise RuntimeError(f"Failed to list crontab: {e.stderr}") from e

    def add_job(self, schedule: str, command: str, description: str) -> str:
        """Adds a new job to the crontab."""
        # We store the description in a comment next to the command
        new_job = f"{schedule} {command} # {description}\n"

        current_cron = self.list_jobs()
        if new_job in current_cron:
            return "Job already exists."

        new_cron = current_cron + new_job
        self._update_crontab(new_cron)
        return f"Successfully added job: {description}"

    def delete_job(self, description_part: str) -> str:
        """Deletes jobs that match a part of their description."""
        current_cron = self.list_jobs().splitlines()
        new_cron_lines = []
        deleted_count = 0

        for line in current_cron:
            if description_part in line and "#" in line:
                deleted_count += 1
                continue
            new_cron_lines.append(line)

        if deleted_count == 0:
            return f"No jobs found matching description: {description_part}"

        self._update_crontab("\n".join(new_cron_lines) + "\n")
        return f"Successfully deleted {deleted_count} job(s) matching: {description_part}"

    def _update_crontab(self, new_cron: str) -> None:
        """Writes the new crontab to the system."""
        process = subprocess.Popen(["crontab", "-"], stdin=subprocess.PIPE, text=True)
        process.communicate(input=new_cron)
        if process.returncode != 0:
            raise RuntimeError(f"Failed to update crontab: {process.stderr}")


if __name__ == "__main__":
    # Quick manual test
    import sys

    cm = CronManager()
    print("Current Jobs:\n", cm.list_jobs(), file=sys.stderr)
    print(cm.add_job("*/5 * * * *", "echo 'hello'", "test-cron-job"), file=sys.stderr)
    print("Updated Jobs:\n", cm.list_jobs(), file=sys.stderr)
    print(cm.delete_job("test-cron-job"), file=sys.stderr)
    print("Final Jobs:\n", cm.list_jobs(), file=sys.stderr)
