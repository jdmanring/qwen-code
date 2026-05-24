from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table


class StatusManager:
    """
    Manly manages the real-time terminal dashboard for the ControlPlane.
    Uses `rich.live.Live` to provide a non-intrusive, professional UI.
    """

    def __init__(self, console: Console | None = None) -> None:
        self.console = console or Console()
        self._live: Live | None = None
        self._active_agent: str | None = None
        self._active_task: str | None = None
        self._job_progress: dict[str, float] = {}  # job_id -> percentage
        self._job_status: dict[str, str] = {}  # job_id -> status string
        self._job_steps: dict[str, list[str]] = {}  # job_id -> list of completed steps
        self.layout = Layout()
        self._setup_layout()

    def _setup_layout(self) -> None:
        """Defines the structure of the dashboard."""
        self.layout.split(
            Layout(name="header", size=3),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=3),
        )
        self.layout.update(self._render_layout())

    def _render_layout(self) -> Layout:
        """Renders the current state into the layout."""
        # Header: System Identity & Active Agent
        header_content = (
            f"[bold cyan]Megalonyx Control Plane[/bold cyan] | "
            f"[bold magenta]Agent: {self._active_agent or 'Idle'}[/bold magenta] | "
            f"[bold yellow]Task: {self._active_task or 'None'}[/bold yellow]"
        )
        self.layout["header"].update(Panel(header_content, border_style="cyan"))

        # Main: Job Progress & Status
        main_content = self._render_main_content()
        self.layout["main"].update(main_content)

        # Footer: System Health & Info
        footer_content = "[dim]System Ready | Mode: Deterministic Orchestration[/dim]"
        self.layout["footer"].update(Panel(footer_content, border_style="dim"))

        return self.layout

    def _render_main_content(self) -> Panel:
        """Renders the central part of the dashboard."""
        if not self._job_status:
            return Panel("[dim]No active jobs. Waiting for command...[/dim]", border_style="dim")

        table = Table(expand=True, box=None)
        table.add_column("Job ID", style="cyan", width=15)
        table.add_column("Status", style="bold", width=15)
        table.add_column("Progress", width=30)
        table.add_column("Last Step", style="dim")

        for job_id, status in self._job_status.items():
            progress = self._job_progress.get(job_id, 0.0)
            last_step = self._job_steps.get(job_id, ["-"])[-1]

            # Use a progress bar for the progress column
            progress_bar = (
                f"[{'#' * int(progress / 10)}{'-' * (10 - int(progress / 10))}] {progress:3.0f}%"
            )

            table.add_row(job_id, status, progress_bar, last_step)

        return Panel(table, title="Active Job Set", border_style="green")

    def start(self) -> None:
        """Starts the live dashboard."""
        if self._live is None:
            self._live = Live(
                self.layout,
                console=self.console,
                refresh_per_second=10,
                transient=False,
            )
            self._live.start()

    def stop(self) -> None:
        """Stops the live dashboard."""
        if self._live:
            self._live.stop()
            self._live = None

    def update_agent(self, agent_name: str, task_name: str) -> None:
        """Updates the header with the current active agent and task."""
        self._active_agent = agent_name
        self._active_task = task_name
        if self._live:
            self._live.update(self._render_layout())

    def update_job_status(
        self, job_id: str, status: str, progress: float = 0.0, last_step: str = ""
    ) -> None:
        """Updates the status and progress of a specific job."""
        self._job_status[job_id] = status
        self._job_progress[job_id] = progress
        if last_step:
            if job_id not in self._job_steps:
                self._job_steps[job_id] = []
            self._job_steps[job_id].append(last_step)

        if self._live:
            self._live.update(self._render_layout())

    def remove_job(self, job_id: str) -> None:
        """Removes a job from the dashboard."""
        self._job_status.pop(job_id, None)
        self._job_progress.pop(job_id, None)
        self._job_steps.pop(job_id, None)
        if self._live:
            self._live.update(self._render_layout())
