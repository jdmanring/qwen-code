from typing import Any

from .job_state_manager import JobStateManager


class SystemWatchdog:
    """
    Monitors the global state to detect stagnation, repetition loops,
    and divergent behavior.
    """

    def __init__(self, state_manager: JobStateManager) -> None:
        self.state_manager = state_manager
        self.history: list[dict[str, Any]] = []  # Stores snapshots of state for trend analysis

    def record_turn(self, agent_name: str, confidence: float, response_hash: str) -> None:
        """Records the outcome of a turn for stagnation analysis."""
        self.history.append({"agent": agent_name, "confidence": confidence, "hash": response_hash})
        # Keep history lean
        if len(self.history) > 20:
            self.history.pop(0)

    def check_for_stagnation(self) -> tuple[bool, str | None]:
        """
        Analyzes history to see if the system is stuck.
        Returns (is_stagnant, reason).
        """
        if len(self.history) < 3:
            return False, None

        # 1. Check for exact repetition (The "Loop" pattern)
        recent_hashes = [h["hash"] for h in self.history[-3:]]
        if len(set(recent_hashes)) == 1:
            return True, "Exact response repetition detected (Livelock)."

        # 2. Check for confidence stagnation
        recent_confidences = [h["confidence"] for h in self.history[-3:]]
        if (
            all(c == recent_confidences[0] for c in recent_confidences)
            and recent_confidences[0] < 0.8
        ):
            return True, "Confidence has plateaued below threshold."

        # 3. Check for "Ping-Pong" behavior (Agent A -> Agent B -> Agent A)
        recent_agents = [h["agent"] for h in self.history[-4:]]
        if (
            len(recent_agents) >= 4
            and recent_agents[0] == recent_agents[2]
            and recent_agents[1] == recent_agents[3]
        ):
            return True, "Agent ping-pong detected (A -> B -> A -> B)."

        return False, None

    def trigger_reflection(self) -> str:
        """Generates a reflection prompt to break the stagnation."""
        return (
            "⚠️ SYSTEM WATCHDOG ALERT: Stagnation detected. "
            "The current approach is not yielding progress. "
            "STOP and perform a meta-analysis: Why is the current strategy failing? "
            "Propose a fundamentally different approach to break the loop."
        )
