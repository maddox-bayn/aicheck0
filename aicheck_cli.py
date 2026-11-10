#!/usr/bin/env python3
"""aicheck0 — Automated Progression Gate & Checkpoint Runner (20 Checkpoints / 200 Exercises)."""

from __future__ import annotations
import argparse
import sys
import pytest

CHECKPOINT_MAP: dict[str, str] = {
    "cp01": "tests/level_1/test_cp_01_primitives_prompts.py",
    "cp02": "tests/level_1/test_cp_02_collections_messages.py",
    "cp03": "tests/level_1/test_cp_03_control_flow_functional.py",
    "cp04": "tests/level_1/test_cp_04_json_env_config.py",
    "cp05": "tests/level_2/test_cp_05_http_rest_fundamentals.py",
    "cp06": "tests/level_2/test_cp_06_llm_sdk_integration.py",
    "cp07": "tests/level_2/test_cp_07_memory_state_management.py",
    "cp08": "tests/level_2/test_cp_08_resilient_cli_chatbot.py",
    "cp09": "tests/level_3/test_cp_09_document_ingestion.py",
    "cp10": "tests/level_3/test_cp_10_chunking_strategies.py",
    "cp11": "tests/level_3/test_cp_11_embeddings_similarity.py",
    "cp12": "tests/level_3/test_cp_12_vector_stores_rag.py",
    "cp13": "tests/level_4/test_cp_13_pydantic_schemas.py",
    "cp14": "tests/level_4/test_cp_14_tool_dispatch_execution.py",
    "cp15": "tests/level_4/test_cp_15_react_agent_loops.py",
    "cp16": "tests/level_4/test_cp_16_multi_agent_orchestration.py",
    "cp17": "tests/level_5/test_cp_17_fastapi_serving.py",
    "cp18": "tests/level_5/test_cp_18_observability_guardrails.py",
    "cp19": "tests/level_5/test_cp_19_automated_llm_evals.py",
    "cp20": "tests/level_5/test_cp_20_production_hardening.py",
}

LEVEL_MAP: dict[str, str] = {
    "level1": "tests/level_1",
    "level2": "tests/level_2",
    "level3": "tests/level_3",
    "level4": "tests/level_4",
    "level5": "tests/level_5",
    "all": "tests",
}


def run_progression_gate() -> int:
    """Run checkpoints sequentially from cp01 to cp20; stop at the first checkpoint that fails."""
    print("=" * 72)
    print("  aicheck0 PROGRESSION GATE — Sequential Checkpoint Verification")
    print("=" * 72)
    for cp_key, test_path in CHECKPOINT_MAP.items():
        print(f"\n>>> Verifying {cp_key.upper()} ({test_path})...")
        code = pytest.main([test_path, "-q", "--tb=line"])
        if code != 0:
            print("\n" + "!" * 72)
            print(f"  [LOCKED] {cp_key.upper()} did not pass all 10 exercises.")
            print(f"  Complete the exercises in {cp_key} and run:")
            print(f"      python aicheck_cli.py {cp_key}")
            print("  before advancing to the next checkpoint!")
            print("!" * 72)
            return code
        print(f"  [PASSED] {cp_key.upper()} — 10/10 exercises verified! Proceeding...")

    print("\n" + "=" * 72)
    print("  CONGRATULATIONS! All 20 Checkpoints (200/200 Exercises) PASSED!")
    print("=" * 72)
    return 0


def main() -> int:
    valid_targets = ["next", *CHECKPOINT_MAP.keys(), *LEVEL_MAP.keys()]
    parser = argparse.ArgumentParser(
        description="aicheck0 — Automated Checkpoint Grader (github.com/maddox-bayn/aicheck0)"
    )
    parser.add_argument(
        "target",
        nargs="?",
        default="next",
        choices=valid_targets,
        help="Target checkpoint (cp01..cp20), level (level1..level5), 'all', or 'next' (sequential progression gate).",
    )
    parser.add_argument(
        "-x", "--fail-fast",
        action="store_true",
        help="Stop immediately on the first failed exercise.",
    )
    args = parser.parse_args()

    if args.target == "next":
        return run_progression_gate()

    target_path = CHECKPOINT_MAP.get(args.target) or LEVEL_MAP[args.target]
    pytest_args = [target_path, "-v"]
    if args.fail_fast:
        pytest_args.append("-x")
    return pytest.main(pytest_args)


if __name__ == "__main__":
    sys.exit(main())
