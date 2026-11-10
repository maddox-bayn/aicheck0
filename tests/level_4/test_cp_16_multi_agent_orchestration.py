"""Automated Pytest Suite for Checkpoint 16 (10 Exercises)."""
import pytest
from checkpoints.level_4_multi_tool_agent.cp_14_tool_dispatch_execution import ToolRegistry
from checkpoints.level_4_multi_tool_agent.cp_16_multi_agent_orchestration import (
    AutonomousAgent, Blackboard, detect_handoff_cycle, execute_handoff_pipeline,
    filter_context_for_agent, majority_vote_ensemble, map_reduce_research,
    route_to_specialist, run_multi_agent_debate, run_supervisor_team,
)

def test_ex_16_01_route_to_specialist():
    name, reply = route_to_specialist("bill issue", lambda _: "billing", {"billing": lambda q: f"Bill:{q}", "general": lambda q: q})
    assert name == "billing" and reply == "Bill:bill issue"

def test_ex_16_02_run_supervisor_team():
    decisions = iter(["researcher", "FINISH"])
    out = run_supervisor_team("Task", lambda _: next(decisions), {"researcher": lambda s: {"notes": "found"}})
    assert out["notes"] == "found"

def test_ex_16_03_execute_handoff_pipeline():
    agents = {
        "triage": lambda q: {"handoff_to": "tech", "context": f"triaged:{q}"},
        "tech": lambda ctx: {"reply": f"solved:{ctx}"},
    }
    assert execute_handoff_pipeline("triage", agents, "bug") == {"reply": "solved:triaged:bug", "final_agent": "tech"}

def test_ex_16_04_map_reduce_research():
    res = map_reduce_research(["q1", "q2"], lambda q: f"ans_{q}", lambda items: "|".join(items))
    assert res == "ans_q1|ans_q2"

def test_ex_16_05_run_multi_agent_debate():
    verdict = run_multi_agent_debate("P", lambda _: "A_view", lambda _: "B_view", lambda p, a, b: f"Judge:{a}+{b}")
    assert "A_view" in verdict and "B_view" in verdict

def test_ex_16_06_filter_context_for_agent():
    hist = [{"role": "system", "content": "S"}, {"role": "user", "content": "ForA", "target_agent": "A"}, {"role": "user", "content": "ForB", "target_agent": "B"}]
    assert len(filter_context_for_agent(hist, "A")) == 2

def test_ex_16_07_blackboard():
    bb = Blackboard()
    v1 = bb.write("plan", "v1_text", "planner")
    assert v1 == 1 and bb.read("plan") == "v1_text"

def test_ex_16_08_majority_vote_ensemble():
    winner, ratio = majority_vote_ensemble([("t1", "42"), ("t2", "42"), ("t3", "41")])
    assert winner == "42" and round(ratio, 2) == 0.67

def test_ex_16_09_detect_handoff_cycle():
    assert detect_handoff_cycle(["A", "B"], "A", max_visits=2) is False
    with pytest.raises(RuntimeError, match="Circular handoff detected"):
        detect_handoff_cycle(["A", "B", "A"], "A", max_visits=2)

def test_ex_16_10_autonomous_agent_milestone():
    reg = ToolRegistry()
    reg.register("add", lambda a, b: a + b)
    steps = iter([
        {"role": "assistant", "tool_calls": [{"id": "1", "function": {"name": "add", "arguments": '{"a": 10, "b": 20}'}}]},
        {"role": "assistant", "content": "Result is 30"},
    ])
    agent = AutonomousAgent(llm_fn=lambda _: next(steps), tools=reg, max_steps=4)
    res = agent.run("Add 10 and 20")
    assert res["answer"] == "Result is 30" and res["tool_calls_made"] == 1
