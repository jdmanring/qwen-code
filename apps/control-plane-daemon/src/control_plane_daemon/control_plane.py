import os
import re
from typing import Any

import yaml
from agent_infra.system_logger import SystemLogger

from .intent_classifier import IntentClassifier
from .job_state_manager import JobStateManager
from .models import Job, JobStatus
from .status_manager import StatusManager
from .task_decomposer import TaskDecomposer
from .verification_engine import VerificationResult


class ControlPlane:
    """
    The Control Plane is the 'Brain' of the system.
    It manages the high-level lifecycle of a user request:
    Intent Classification -> Task Decomposition -> Job State Management.
    """

    def __init__(self, settings_path: str | None = None) -> None:
        self.logger = SystemLogger()
        self.classifier = IntentClassifier(settings_path)
        self.decomposer = TaskDecomposer(settings_path)
        self.jsm = JobStateManager(settings_path)
        self.status_manager = StatusManager()

        # Initialize Workflow & Skill Management
        from .command_manager import CommandManager
        from .execution_profile_selector import ExecutionProfileSelector

        self.command_manager = CommandManager()
        self.execution_profile_selector = ExecutionProfileSelector()

        # Initialize Verification Engine
        from .verification_contracts import (
            DiscoveryContract,
            DynamicVerificationContract,
            MutationContract,
            SynthesisContract,
        )
        from .verification_engine import VerificationEngine

        self.ve = VerificationEngine(self.jsm, settings_path=settings_path)
        self.ve.register_contract("mutation", MutationContract())
        self.ve.register_contract("discovery", DiscoveryContract())
        self.ve.register_contract("synthesis", SynthesisContract())
        self.ve.register_contract("dynamic", DynamicVerificationContract())

        # Initialize Policy Engine
        from .policy_engine import PolicyEngine

        self.policy_engine = PolicyEngine(settings_path=settings_path)

    def process_intent(self, prompt: str) -> dict[str, Any]:
        """
        Processes a raw user prompt into a managed set of jobs.
        Supports both natural language intents and slash-commands.
        """
        self.logger.info("control_plane_start", {"prompt": prompt})

        # 1. Check for Slash-Commands
        if prompt.startswith("/"):
            cmd_part = prompt.lstrip("/").split(" ", 1)
            cmd_id = cmd_part[0]
            cmd_args = cmd_part[1] if len(cmd_part) > 1 else ""

            command = self.command_manager.get_command(cmd_id)
            if command:
                self.logger.info(
                    "command_triggered",
                    {
                        "command": cmd_id,
                        "args": cmd_args,
                        "description": command["description"],
                    },
                )

                # For commands, we bypass standard decomposition and use the workflow
                # We create a special 'workflow' job set
                jobs = [
                    {
                        "job_id": "workflow_root",
                        "description": f"Execute {cmd_id} workflow",
                        "assigned_skill": "orchestrator",
                        "job_type": "workflow",
                        "verification_criteria": "Workflow completion",
                    }
                ]
                job_set = self.jsm.initialize_job_set(jobs)
                self.status_manager.update_job_status(
                    "workflow_root", JobStatus.PENDING, 0.0, "Initializing workflow"
                )

                return {
                    "intent": f"command:{cmd_id}",
                    "job_set": job_set,
                    "command_workflow": command,
                }
        # 2. Standard Intent Classification (Fallback)
        classification = self.classifier.classify(prompt)
        intent_name = classification["intent"]
        self.logger.info(
            "intent_classified",
            {
                "intent": intent_name,
                "reasoning": classification.get("reasoning", "No reasoning provided"),
                "risk": classification.get("risk_profile", "Unknown"),
            },
        )

        # 3. Job Contract Creation
        job_contract = {
            "intent": intent_name,
            "risk_profile": classification["risk_profile"],
            "suggested_tool_chain": classification["suggested_tool_chain"],
            "original_prompt": prompt,
        }

        # 4. Task Decomposition
        jobs = self.decomposer.decompose(job_contract)
        self.logger.info(
            "tasks_decomposed",
            {"job_count": len(jobs), "jobs": [j["description"] for j in jobs]},
        )

        # 5. Job Set Initialization
        job_set = self.jsm.initialize_job_set(jobs)
        self.logger.info("job_set_initialized", {"job_set_id": "active_job_set"})

        if jobs:
            self.status_manager.update_job_status(
                jobs[0]["job_id"], JobStatus.PENDING, 0.0, "Starting decomposition"
            )

        return {
            "intent": intent_name,
            "job_set": job_set,
            "classification": classification,
        }

    def get_next_job(self) -> dict[str, Any] | None:
        """Retrieves the next executable job from the state manager."""
        return self.jsm.get_next_job()

    def update_job(self, job_id: str, status: JobStatus, result: Any = None) -> None:
        """Updates the status of a job and persists it."""
        self.jsm.update_job_status(job_id, status, result)

    def is_complete(self) -> bool:
        """Checks if all jobs in the current set are completed."""
        return self.jsm.is_task_complete()

    def clear(self) -> None:
        """Clears the current job set."""
        self.jsm.clear_jobs()

    async def _spawn_agent(
        self,
        agent_id: str,
        task_prompt: str,
        model_id: str,
        settings: dict,
        search_tool: Any,
        root_context: Any,
    ) -> str:
        """
        Spawns a specialized agent persona to handle a specific sub-task.
        Returns the agent's structured report.
        """
        self.logger.info("agent_spawned", {"agent_id": agent_id, "task": task_prompt})

        # Update status manager
        self.status_manager.update_agent(agent_id, task_prompt[:50])

        # 1. Load Agent Persona
        agent_path = os.path.expanduser(f"~/.qwen/agents/{agent_id}.md")
        if not os.path.exists(agent_path):
            self.logger.error("agent_not_found", {"agent_id": agent_id, "path": agent_path})
            return f"Error: Agent {agent_id} not found."

        with open(agent_path, encoding="utf-8") as f:
            persona_content = f.read()

        # 2. Construct the Agent Config
        # We wrap the persona in a config that run_job_execution expects
        agent_config = {
            "name": agent_id,
            "system_prompt": persona_content,
            "tools": [],  # The agent uses the tools available in the core engine
        }

        # 3. Execute as a single-shot job
        # We create a temporary job object for the bridge
        temp_job = {
            "job_id": f"spawned_{agent_id}",
            "description": task_prompt,
            "assigned_skill": agent_id,
            "job_type": "specialist",
            "verification_criteria": "Structured report provided",
        }

        from .tool_executor import run_job_execution

        response = await run_job_execution(
            temp_job,
            task_prompt,
            agent_config,
            model_id,
            settings,
            self.jsm,
            search_tool,
            self.policy_engine,
            "specialist",
            context=root_context.clone(),
            history=[{"role": "user", "content": task_prompt}],
        )

        return response

    async def execute_workflow(
        self,
        cmd_id: str,
        prompt: str,
        model_id: str,
        settings: dict,
        search_tool: Any,
        root_context: Any,
    ) -> str:
        """
        Interprets and executes a Markdown-based workflow from a command.
        """
        command = self.command_manager.get_command(cmd_id)
        if not command:
            return f"Error: Command {cmd_id} not found."

        workflow_body = command["workflow"]

        # Simple workflow interpretation:
        # We look for "Spawn the [agent] agent" patterns in the markdown.
        # In a full implementation, this would be a more robust parser.

        full_execution_log = f"# Workflow Execution: {cmd_id}\n\n"
        current_context = prompt

        # Split workflow into sections (e.g., Step 1, Step 2)
        steps = re.split(r"## Step \d+:|### \d+\.", workflow_body)
        # The first element is usually the intro, so we skip it
        steps = [s.strip() for s in steps[1:] if s.strip()]

        for i, step in enumerate(steps):
            job_id = f"workflow_step_{i + 1}"
            self.status_manager.update_job_status(job_id, "running", 0.0, f"Step {i + 1}")

            # Handle Todo Operations
            todo_match = re.search(r"TODO_OP: (list|add|done) (.*)", step, re.IGNORECASE)
            if todo_match:
                subcommand = todo_match.group(1).lower()
                args = todo_match.group(2).strip()

                result = ""
                if subcommand == "list":
                    tasks = self.jsm.list_tasks()
                    result = "\n".join(
                        [
                            f"[{'x' if t['status'] == 'completed' else ' '}] "
                            f"{t['id']}: {t['content']}"
                            for t in tasks
                        ]
                    )
                elif subcommand == "add":
                    tid = self.jsm.add_task(args)
                    result = f"Added task: {tid}"
                elif subcommand == "done":
                    success = self.jsm.complete_task(args)
                    result = "Task completed" if success else f"Task {args} not found"

                full_execution_log += (
                    f"## Step {i + 1} (Todo Operation: {subcommand})\n{result}\n\n"
                )
                current_context += f"\n\nStep {i + 1} Result: {result}"
                self.status_manager.update_job_status(
                    job_id, "completed", 100.0, f"Step {i + 1} Done"
                )
                continue

            # Check if this step requires a specialized agent
            agent_match = re.search(r"Spawn the ([a-zA-Z0-9_-]+) agent", step, re.IGNORECASE)
            if agent_match:
                agent_id = agent_match.group(1).lower().replace(" ", "-")
                # Construct a task prompt for the agent based on the step description
                task_prompt = f"WORKFLOW STEP {i + 1}: {step}\n\nINPUT CONTEXT: {current_context}"

                self.status_manager.update_agent(agent_id, step[:50])
                agent_report = await self._spawn_agent(
                    agent_id, task_prompt, model_id, settings, search_tool, root_context
                )

                full_execution_log += f"## Step {i + 1} (Agent: {agent_id})\n{agent_report}\n\n"
                current_context += f"\n\nStep {i + 1} Result: {agent_report}"
                self.status_manager.update_job_status(
                    job_id, "completed", 100.0, f"Step {i + 1} Done"
                )
            else:
                # Standard execution using the general orchestrator
                # We treat this as a normal job
                job = {
                    "job_id": job_id,
                    "description": step,
                    "assigned_skill": "orchestrator",
                    "job_type": "general",
                    "verification_criteria": "Step completion",
                }

                from .tool_executor import run_job_execution

                res = await run_job_execution(
                    job,
                    step,
                    None,
                    model_id,
                    settings,
                    self.jsm,
                    search_tool,
                    self.policy_engine,
                    "general",
                    context=root_context.clone(),
                    history=[{"role": "user", "content": step}],
                )
                full_execution_log += f"## Step {i + 1} (Orchestrator)\n{res}\n\n"
                current_context += f"\n\nStep {i + 1} Result: {res}"
                self.status_manager.update_job_status(
                    job_id, "completed", 100.0, f"Step {i + 1} Done"
                )

        return full_execution_log

    async def execute(
        self,
        prompt: str,
        model_id: str,
        settings: dict,
        search_tool: Any,
        root_context: Any,
    ) -> str:
        """
        Executes the decomposed job set using a deterministic loop:
        Act -> Observe -> Verify -> Correct.
        """
        from .tool_executor import run_job_execution

        final_aggregated_response = ""
        global_retry_count = 0
        GLOBAL_RETRY_LIMIT = 10
        job_histories = {}  # Maintain history across retries and pivots for each job

        while not self.is_complete():
            job = self.get_next_job()
            if not job:
                self.logger.info("job_loop_exhausted", {})
                break

            job_id = job["job_id"]
            self.logger.info("job_loop_processing", {"job_id": job_id})
            self.status_manager.update_job_status(
                job_id, JobStatus.RUNNING, 0.0, job["description"][:50]
            )

            # HANDLE WORKFLOW JOBS
            if job.get("job_type") == "workflow":
                self.logger.info("workflow_execution_start", {"job_id": job_id})

                # Extract command ID from the intent (e.g., "command:bugfix" -> "bugfix")
                # We need to pass the original prompt to the workflow as context
                intent = (
                    self.classifier.classify(prompt)["intent"]
                    if not prompt.startswith("/")
                    else prompt.lstrip("/").split(" ")[0]
                )
                cmd_id = intent.replace("command:", "") if "command:" in intent else intent

                workflow_result = await self.execute_workflow(
                    cmd_id, prompt, model_id, settings, search_tool, root_context
                )

                self.update_job(job_id, JobStatus.COMPLETED, result=workflow_result)
                self.status_manager.update_job_status(
                    job_id, JobStatus.COMPLETED, 100.0, "Workflow complete"
                )
                final_aggregated_response += f"\\n\\n{workflow_result}"
                continue

            self.logger.info(
                "job_execution_start",
                {"job_id": job_id, "description": job["description"]},
            )

            # 1. Resolve skill config
            skill_config = None
            runtime_root = os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            )
            service_file = os.path.join(
                runtime_root, "config", "services", f"{job['assigned_skill']}.yaml"
            )
            if os.path.exists(service_file):
                with open(service_file) as f:
                    raw_config = yaml.safe_load(f)
                    skill_config = {
                        "name": raw_config["name"],
                        "system_prompt": raw_config.get("persona", {}).get("system_prompt", ""),
                        "tools": raw_config.get("capabilities", {}).get("tools", []),
                    }

            # 2. Manage Job History
            if job_id not in job_histories:
                job_prompt = (
                    f"TASK: {job['description']}\\nCONTEXT: {prompt}\\n"
                    f"JOB_ID: {job_id}\\nREQUIRED_OUTCOME: {job['verification_criteria']}"
                )
                job_histories[job_id] = [{"role": "user", "content": job_prompt}]

            history = job_histories[job_id]

            # 3. ACT: Execute the job
            # The current history includes the original prompt and any previous failure logs
            try:
                job_response = await run_job_execution(
                    job,
                    history[-1]["content"] if history else prompt,
                    skill_config,
                    model_id,
                    settings,
                    self.jsm,
                    search_tool,
                    self.policy_engine,
                    job["job_type"],
                    context=root_context.clone(),
                    history=history,
                )
            except (BrokenPipeError, ConnectionResetError, OSError) as e:
                self.logger.error(
                    "job_execution_transport_failure", {"job_id": job_id, "error": str(e)}
                )
                # Treat transport failure as a verification failure to trigger the correction loop
                job_response = f"Transport Error: {str(e)}"

                v_result = VerificationResult(
                    is_success=False,
                    confidence=1.0,
                    logs=f"Transport failure: {str(e)}",
                    suggested_action="RETRY",
                )

                # Skip to correction logic
                global_retry_count += 1
                if global_retry_count >= GLOBAL_RETRY_LIMIT:
                    self.update_job(job_id, JobStatus.FAILED, result=job_response)
                    self.status_manager.update_job_status(
                        job_id, JobStatus.FAILED, 0.0, "Failed: Limit reached"
                    )
                    self._fail_all_pending()
                    break

                correction_prompt = (
                    f"TRANSPORT FAILURE for Job {job_id}:\\n{v_result.logs}\\n\\n"
                    "Please check the service status and retry."
                )
                history.append({"role": "user", "content": correction_prompt})
                self.update_job(job_id, JobStatus.RETRYING, result=job_response)
                self.status_manager.update_job_status(
                    job_id, JobStatus.RETRYING, 50.0, "Retrying..."
                )
                continue

            history.append({"role": "assistant", "content": job_response})

            # 4. OBSERVE & VERIFY: Check against contract
            v_type = job["job_type"]
            if job.get("verification_criteria") and any(
                cmd in job["verification_criteria"]
                for cmd in ["pytest", "mypy", "npm test", "go test"]
            ):
                v_type = "dynamic"

            v_context: dict[str, Any] = {
                "project_root": runtime_root,
                "requested_symbols": [],
                "verification_criteria": job.get("verification_criteria"),
            }
            v_result = self.ve.verify_job(job_id, v_type, job_response, context=v_context)

            if v_result.is_success:
                self.update_job(job_id, JobStatus.COMPLETED, result=job_response)
                self.status_manager.update_job_status(
                    job_id, JobStatus.COMPLETED, 100.0, "Verified"
                )

                final_aggregated_response += f"\\n\\nJob {job_id} completed: {job_response}"
            else:
                # 5. CORRECT: Handle failure based on suggested action
                global_retry_count += 1
                if global_retry_count >= GLOBAL_RETRY_LIMIT:
                    self.logger.error("global_retry_limit_reached", {"limit": GLOBAL_RETRY_LIMIT})
                    self.update_job(job_id, JobStatus.FAILED, result=job_response)
                    self.status_manager.update_job_status(
                        job_id, JobStatus.FAILED, 0.0, "Failed: Limit reached"
                    )
                    self._fail_all_pending()
                    break

                self.logger.warn(
                    "job_verification_failed",
                    {
                        "job_id": job_id,
                        "error": v_result.logs,
                        "action": v_result.suggested_action,
                    },
                )

                if v_result.suggested_action == "PIVOT":
                    # Create a correction job for the specific failure
                    corr_job_data = self.decomposer.create_correction_job(job, v_result.logs)
                    corr_job = Job(**corr_job_data)
                    self.jsm.add_job(corr_job)

                    # Execute the correction job immediately
                    corr_response = await self._execute_single_job(
                        corr_job, model_id, settings, search_tool, root_context
                    )

                    # Feed the correction result back into the original job's history
                    pivot_prompt = (
                        f"CORRECTION JOB RESULT for {corr_job['job_id']}:\\n{corr_response}\\n\\n"
                        f"Original failure: {v_result.logs}. "
                        f"Please provide the final corrected implementation for Job {job_id}."
                    )
                    history.append({"role": "user", "content": pivot_prompt})

                    self.update_job(job_id, JobStatus.RETRYING, result=job_response)
                    self.status_manager.update_job_status(
                        job_id, JobStatus.RETRYING, 50.0, "Correcting..."
                    )

                elif v_result.suggested_action == "ABORT":
                    self.logger.info("abort_suggested", {"job_id": job_id})
                    self.update_job(job_id, JobStatus.FAILED, result=job_response)
                    self.status_manager.update_job_status(job_id, JobStatus.FAILED, 0.0, "Aborted")
                    self._fail_all_pending()
                    break

                else:  # Default to RETRY
                    correction_prompt = (
                        f"VERIFICATION FAILURE for Job {job_id}:\\n{v_result.logs}\\n\\n"
                        "Please analyze the failure and provide a corrected implementation."
                    )
                    history.append({"role": "user", "content": correction_prompt})
                    self.update_job(job_id, JobStatus.RETRYING, result=job_response)
                    self.status_manager.update_job_status(
                        job_id, JobStatus.RETRYING, 50.0, "Retrying..."
                    )

        # Cleanup
        self.status_manager.update_agent("Idle", "None")
        for job_id in list(self.jsm.sm.get("active_job_set", {}).get("jobs", {}).keys()):
            self.status_manager.remove_job(job_id)

        return final_aggregated_response

    def _fail_all_pending(self) -> None:
        """Marks all pending jobs in the active set as failed."""
        job_set = self.jsm.sm.get("active_job_set", {})
        for j_id, j_val in job_set.get("jobs", {}).items():
            if j_val["status"] == JobStatus.PENDING:
                self.update_job(j_id, JobStatus.FAILED)
                self.status_manager.update_job_status(j_id, JobStatus.FAILED, 0.0, "Failed")

    async def _execute_single_job(
        self,
        job: dict[str, Any],
        model_id: str,
        settings: dict[str, Any],
        search_tool: Any,
        root_context: Any,
    ) -> str:
        """Helper to execute a single job (used for pivots) without updating the main loop state."""
        from .tool_executor import run_job_execution

        skill_config = None
        runtime_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        service_file = os.path.join(
            runtime_root, "config", "services", f"{job['assigned_skill']}.yaml"
        )
        if os.path.exists(service_file):
            with open(service_file) as f:
                raw_config = yaml.safe_load(f)
                skill_config = {
                    "name": raw_config["name"],
                    "system_prompt": raw_config.get("persona", {}).get("system_prompt", ""),
                    "tools": raw_config.get("capabilities", {}).get("tools", []),
                }

        prompt = f"TASK: {job['description']}\\nREQUIRED_OUTCOME: {job['verification_criteria']}"
        return await run_job_execution(
            job,
            prompt,
            skill_config,
            model_id,
            settings,
            self.jsm,
            search_tool,
            self.policy_engine,
            job["job_type"],
            context=root_context.clone(),
            history=[{"role": "user", "content": prompt}],
        )
