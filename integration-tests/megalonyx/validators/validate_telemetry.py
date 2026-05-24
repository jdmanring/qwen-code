import json
import os
from collections import Counter

LOG_FILE = "storage/system.log"


def analyze_logs() -> None:
    if not os.path.exists(LOG_FILE):
        print(f"Log file {LOG_FILE} not found.")
        return

    events = []
    with open(LOG_FILE) as f:
        for line in f:
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    # Analysis
    event_types = Counter([e.get("event") for e in events])
    agents = Counter(
        [e.get("data", {}).get("agent") for e in events if "agent" in e.get("data", {})]
    )
    guards = Counter(
        [
            e.get("data", {}).get("reason")
            for e in events
            if e.get("event") == "guard_triggered"
        ]
    )
    phases = Counter(
        [
            e.get("data", {}).get("to")
            for e in events
            if e.get("event") == "phase_transition"
        ]
    )

    print("=== QWEN-CODE-STACK TELEMETRY REPORT ===")
    print(f"\nTotal Events Captured: {len(events)}")

    print("\n--- Event Distribution ---")
    for event, count in event_types.items():
        print(f"{event:25}: {count}")

    print("\n--- Agent Activity ---")
    for agent, count in agents.items():
        print(f"{agent:25}: {count} activations")

    print("\n--- Guard Triggers ---")
    if not guards:
        print("No guard triggers detected. (Clean workflow)")
    for reason, count in guards.items():
        print(f"{reason:25}: {count} times")

    print("\n--- Phase Transitions ---")
    for phase, count in phases.items():
        print(f"Entered {phase:18}: {count} times")
    print("\n" + "=" * 40)


if __name__ == "__main__":
    analyze_logs()
