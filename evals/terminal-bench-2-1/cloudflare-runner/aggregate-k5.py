"""Validate and aggregate the five V16 fix 4 Terminal-Bench replicates."""

from __future__ import annotations

import json
import math
from pathlib import Path
from statistics import mean, stdev
from typing import Any


ROOT = Path(__file__).resolve().parent
RUNS = ROOT / "runs"
EXPECTED_VERSION = "v16-explicit-maintenance-fix4"
RUN_NAMES = [
    "terminal-bench-2.1-k1-luna-max-v16-fix4-final",
    "terminal-bench-2.1-k5-luna-max-v16-fix4-r2",
    "terminal-bench-2.1-k5-luna-max-v16-fix4-r3",
    "terminal-bench-2.1-k5-luna-max-v16-fix4-r4",
    "terminal-bench-2.1-k5-luna-max-v16-fix4-r5",
]
OUTPUT = RUNS / "terminal-bench-2.1-k5-luna-max-v16-fix4-summary.json"


def load_state(run_name: str) -> dict[str, Any]:
    path = RUNS / run_name / "state.json"
    if not path.is_file():
        raise RuntimeError(f"missing state: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def collect_versions(value: Any) -> set[str]:
    versions: set[str] = set()
    if isinstance(value, dict):
        agent_info = value.get("agent_info")
        if isinstance(agent_info, dict) and isinstance(agent_info.get("version"), str):
            versions.add(agent_info["version"])
        for child in value.values():
            versions.update(collect_versions(child))
    elif isinstance(value, list):
        for child in value:
            versions.update(collect_versions(child))
    return versions


def validate_run(run_name: str, state: dict[str, Any]) -> dict[str, float]:
    tasks = state.get("tasks")
    if not isinstance(tasks, dict) or len(tasks) != 89:
        raise RuntimeError(f"{run_name}: expected 89 tasks")

    incomplete = [
        name for name, entry in tasks.items() if entry.get("phase") != "completed"
    ]
    if incomplete:
        raise RuntimeError(f"{run_name}: incomplete tasks: {incomplete[:5]}")

    rewards = [entry.get("reward") for entry in tasks.values()]
    if any(reward not in {0, 0.0, 1, 1.0} for reward in rewards):
        raise RuntimeError(f"{run_name}: invalid reward values")

    # Validate only the accepted final outcome for each task. Historical
    # infrastructure attempts are retained under ``last_error`` and may carry
    # incomplete/unknown diagnostics; they are not valid benchmark outcomes.
    versions = {
        version
        for entry in tasks.values()
        for version in collect_versions(entry.get("status"))
    }
    declared_version = state.get("agent_version")
    if declared_version:
        versions.add(str(declared_version))
    if versions != {EXPECTED_VERSION}:
        raise RuntimeError(f"{run_name}: unexpected agent versions: {sorted(versions)}")

    return {name: float(entry["reward"]) for name, entry in tasks.items()}


def main() -> int:
    runs = {name: validate_run(name, load_state(name)) for name in RUN_NAMES}
    task_names = set(next(iter(runs.values())))
    if any(set(results) != task_names for results in runs.values()):
        raise RuntimeError("task sets differ across replicates")

    per_task = {
        task: [runs[run_name][task] for run_name in RUN_NAMES]
        for task in sorted(task_names)
    }
    task_rates = [mean(rewards) for rewards in per_task.values()]
    total_passes = int(sum(sum(rewards) for rewards in per_task.values()))
    total_trials = 89 * 5
    score = total_passes / total_trials
    clustered_se = stdev(task_rates) / math.sqrt(len(task_rates))
    margin = 1.96 * clustered_se

    summary = {
        "dataset": "terminal-bench-2.1",
        "agent_version": EXPECTED_VERSION,
        "model": "gpt-5.6-luna",
        "reasoning_effort": "max",
        "k": 5,
        "tasks": 89,
        "valid_trials": total_trials,
        "passes": total_passes,
        "score": score,
        "clustered_standard_error": clustered_se,
        "clustered_95_percent_interval": [
            max(0.0, score - margin),
            min(1.0, score + margin),
        ],
        "runs": RUN_NAMES,
        "per_task": {
            task: {"rewards": rewards, "passes": int(sum(rewards))}
            for task, rewards in per_task.items()
        },
    }
    OUTPUT.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(
        json.dumps(
            {key: value for key, value in summary.items() if key != "per_task"},
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
