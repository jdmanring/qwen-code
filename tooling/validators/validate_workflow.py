import json
import os
from collections import defaultdict

LOG_FILE = "storage/system.log"


def audit_workflow() -> None:
    if not os.path.exists(LOG_FILE):
        print(f"Log file {LOG_FILE} not found. No data to audit.")
        return

    session_reads = defaultdict(set)
    violations = []
    delegations = 0
    total_edits = 0
    rule_violations = []

    print("=== AGENTIC WORKFLOW AUDIT ===")

    with open(LOG_FILE) as f:
        for line in f:
            try:
                event = json.loads(line)
                evt_type = event.get("event")
                data = event.get("data", {})

                # 1. Track Delegations (UI Indicators)
                if evt_type == "agent_activation":
                    delegations += 1
                    print(f"✅ Delegation Detected: {data.get('agent')} activated.")

                # 2. Track Reads
                if evt_type == "tool_call" and data.get("tool") == "read_file":
                    path = data.get("args", {}).get("file_path")
                    if path:
                        session_reads[data.get("agent", "primary")].add(path)

                # 3. Audit Edits (The "Read-Before-Edit" Check)
                if evt_type == "tool_call" and data.get("tool") == "edit":
                    total_edits += 1
                    path = data.get("args", {}).get("file_path")
                    agent = data.get("agent", "primary")

                    if path not in session_reads[agent]:
                        violations.append(
                            f"Violation: Agent {agent} edited {path} without reading it first."
                        )
                    else:
                        print(f"✅ Professional Sequence: {agent} read then edited {path}.")

                # 4. Audit Tool Permissions (Tavily Check)
                if evt_type == "tool_call" and "tavily" in data.get("tool", ""):
                    agent = data.get("agent", "primary")
                    if agent == "primary":
                        rule_violations.append(
                            "RULE VIOLATION: Primary Agent used Tavily directly (Forbidden)."
                        )
                    else:
                        print(f"✅ Authorized Research: {agent} used Tavily.")

            except json.JSONDecodeError:
                continue

    print("\n" + "=" * 40)
    print(f"Total Delegations: {delegations}")
    print(f"Total Edits Attempted: {total_edits}")

    if not violations:
        print(
            "\n🏆 WORKFLOW VERIFIED: All edits were preceded by a read. No 'blind edits' detected."
        )
    else:
        print("\n❌ WORKFLOW FAILED: Blind edits detected!")
        for v in violations:
            print(f" - {v}")

    if not rule_violations:
        print("✅ PERMISSIONS VERIFIED: No unauthorized tool use detected.")
    else:
        print("\n🚨 PERMISSION VIOLATIONS DETECTED:")
        for rv in rule_violations:
            print(f" - {rv}")
    print("=" * 40)


if __name__ == "__main__":
    audit_workflow()
