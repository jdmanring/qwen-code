import asyncio
import json
import os
import shutil
import tempfile
import time
from unittest.mock import MagicMock, patch

from control_plane_daemon.control_plane import ControlPlane


class LatencyBench:
    """
    Benchmarks the latency of the Control Plane orchestration loop.
    Measures the time for Intent Classification -> Decomposition -> First Job Execution.
    """

    def __init__(self):
        self.test_dir = tempfile.mkdtemp(prefix="megalonyx-bench-")
        self.settings_path = os.path.join(self.test_dir, "settings.json")
        self.setup_environment()

    def setup_environment(self):
        settings = {
            "fastModel": "gemini-2.5-flash-lite",
            "modelProviders": {
                "google": [{"id": "gemini-2.5-flash-lite", "baseUrl": "...", "envKey": "..."}]
            },
        }
        with open(self.settings_path, "w") as f:
            json.dump(settings, f)

    def cleanup(self):
        shutil.rmtree(self.test_dir)

    async def measure_turn_latency(
        self, prompt: str, mock_intent: dict, mock_execution_result: str
    ) -> dict[str, float]:
        cp = ControlPlane(settings_path=self.settings_path)

        mock_context = MagicMock()
        mock_context.clone.return_value = mock_context
        mock_search_tool = MagicMock()

        # We measure the time from the start of process_intent to the end of the first job execution
        start_time = time.perf_counter()

        with (
            patch("litellm.completion") as mock_completion,
            patch("control_plane_daemon.tool_executor.run_job_execution") as mock_executor,
            patch.object(cp.ve, "verify_job") as mock_verify,
        ):
            mock_completion.return_value.choices[0].message.content = json.dumps(mock_intent)
            mock_executor.return_value = mock_execution_result

            mock_v_result = MagicMock()
            mock_v_result.is_success = True
            mock_verify.return_value = mock_v_result

            # 1. Measure Intent Classification + Decomposition
            cp.process_intent(prompt)
            decomposition_time = time.perf_counter() - start_time

            # 2. Measure First Job Execution
            exec_start = time.perf_counter()
            cp.execute(
                prompt=prompt,
                model_id="gemini-2.5-flash-lite",
                settings=json.load(open(self.settings_path)),
                search_tool=mock_search_tool,
                root_context=mock_context,
            )
            execution_time = time.perf_counter() - exec_start

            total_time = time.perf_counter() - start_time

        return {
            "decomposition_latency": decomposition_time,
            "execution_latency": execution_time,
            "total_latency": total_time,
        }


async def main():
    bench = LatencyBench()
    scenarios = [
        {
            "name": "Targeted Bugfix",
            "prompt": "Fix the bug in utils.py",
            "intent": {
                "intent": "Targeted Bugfix",
                "risk_profile": "Low",
                "suggested_tool_chain": ["read_file"],
            },
            "result": "Fixed bug.",
        },
        {
            "name": "Feature Implementation",
            "prompt": "Add CSV export",
            "intent": {
                "intent": "Feature Implementation",
                "risk_profile": "Med",
                "suggested_tool_chain": ["edit"],
            },
            "result": "Implemented feature.",
        },
        {
            "name": "Architectural Refactor",
            "prompt": "Refactor auth module",
            "intent": {
                "intent": "Architectural Refactor",
                "risk_profile": "High",
                "suggested_tool_chain": ["review"],
            },
            "result": "Refactored architecture.",
        },
    ]

    print(f"{'Scenario':<25} | {'Decomp (s)':<12} | {'Exec (s)':<12} | {'Total (s)':<12}")
    print("-" * 65)

    all_results = {}
    for s in scenarios:
        # Run multiple iterations to get an average
        iterations = 5
        total_decomp = 0
        total_exec = 0
        total_all = 0

        for _ in range(iterations):
            res = await bench.measure_turn_latency(s["prompt"], s["intent"], s["result"])
            total_decomp += res["decomposition_latency"]
            total_exec += res["execution_latency"]
            total_all += res["total_latency"]

        avg_decomp = total_decomp / iterations
        avg_exec = total_exec / iterations
        avg_all = total_all / iterations

        print(f"{s['name']:<25} | {avg_decomp:<12.4f} | {avg_exec:<12.4f} | {avg_all:<12.4f}")
        all_results[s["name"]] = {
            "decomposition": avg_decomp,
            "execution": avg_exec,
            "total": avg_all,
        }

    bench.cleanup()

    # Save baselines to a file
    with open("latency_baselines.json", "w") as f:
        json.dump(all_results, f, indent=2)
    print("\nBaselines saved to latency_baselines.json")


if __name__ == "__main__":
    asyncio.run(main())
