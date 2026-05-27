from enum import StrEnum
from typing import Any, Literal

from pydantic import BaseModel, Field


class JobStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    RETRYING = "retrying"
    PIVOTING = "pivoting"
    COMPLETED = "completed"
    FAILED = "failed"


class JobType(StrEnum):
    GENERAL = "general"
    SPECIALIST = "specialist"
    WORKFLOW = "workflow"
    CORRECTION = "correction"


class Job(BaseModel):
    job_id: str
    description: str
    assigned_skill: str
    job_type: JobType
    verification_criteria: str
    status: JobStatus = JobStatus.PENDING
    result: Any | None = None
    dependencies: list[str] = Field(default_factory=list)
    updated_at: str | None = None


class JobSet(BaseModel):
    start_time: str
    jobs: dict[str, Job]


class ToolRequest(BaseModel):
    tool_name: str
    args: dict[str, Any]


class ToolResponse(BaseModel):
    success: bool
    content: Any
    error: str | None = None


class VerificationResult(BaseModel):
    is_success: bool
    suggested_action: Literal["RETRY", "PIVOT", "ABORT"]
    logs: str


class Policy(BaseModel):
    allowed_tools: list[str]
    allowed_paths: list[str]
    can_write: bool = False
    verification_level: str = "Low"
    approval_required: bool = False


class SkillConfig(BaseModel):
    name: str
    system_prompt: str
    tools: list[str] = Field(default_factory=list)
