"""Automated Pytest Suite for Checkpoint 15 (10 Exercises)."""
from checkpoints.level_4_multi_tool_agent.cp_14_tool_dispatch_execution import ToolRegistry
from checkpoints.level_4_multi_tool_agent.cp_15_react_agent_loops import (
    AgentTrace, StateGraphEngine, check_agent_budget, execute_with_human_approval,
    parse_react_step, run_agent_loop, run_plan_and_execute, run_reflexion_loop,
    save_and_resume_checkpoint, update_plan_on_failure,
)

def test_ex_15_01_run_agent_loop():
    reg = ToolRegistry()
    reg.register("mul", lambda a, b: a * b)
    turns = iter([
        {"role": "assistant", "tool_calls": [{"id": "c1", "function": {"name": "mul", "arguments": '{"a": 6, "b": 7}'}}]},
        {"role": "assistant", "content": "The product is 42."},
    ])
    ans = run_agent_loop(lambda _: next(turns), reg, [{"role": "user", "content": "6*7?"}])
    assert ans == "The product is 42."

def test_ex_15_02_parse_react_step():
    s1 = parse_react_step('Thought: Need math\nAction: calc\nAction Input: {"x": 5}')
    assert s1["type"] == "action" and s1["tool"] == "calc" and s1["input"] == {"x": 5}
    s2 = parse_react_step("Thought: Done\nFinal Answer: 42")
    assert s2["type"] == "final" and s2["answer"] == "42"

def test_ex_15_03_agent_trace():
    t = AgentTrace()
    t.log_step({"tool": "calc", "latency_ms": 12.5})
    d = t.to_dict()
    assert d["total_steps"] == 1 and d["total_latency_ms"] == 12.5

def test_ex_15_04_execute_with_human_approval():
    reg = ToolRegistry()
    reg.register("delete_db", lambda: "deleted")
    assert execute_with_human_approval("delete_db", {}, reg, {"delete_db"}, lambda n, a: False) == "REJECTED_BY_HUMAN"
    assert execute_with_human_approval("delete_db", {}, reg, {"delete_db"}, lambda n, a: True) == "deleted"

def test_ex_15_05_run_plan_and_execute():
    res = run_plan_and_execute("Build", lambda _: ["s1", "s2"], lambda s, prev: f"done_{s}")
    assert res["results"] == ["done_s1", "done_s2"]

def test_ex_15_06_update_plan_on_failure():
    new_steps = update_plan_on_failure(["s1", "s2"], [("s1", "ok")], "s2", "err", lambda *_: ["s2_alt"])
    assert new_steps == ["s2_alt"]

def test_ex_15_07_run_reflexion_loop():
    out = run_reflexion_loop(
        "Write code",
        actor_fn=lambda p, fb: "good_code" if fb else "bad_code",
        critic_fn=lambda p, d: (d == "good_code", "Fix bug"),
    )
    assert out == "good_code"

def test_ex_15_08_check_agent_budget():
    assert check_agent_budget(100, 0.01, 1000, 1.0) == (True, "OK")
    assert check_agent_budget(2000, 0.01, 1000, 1.0)[0] is False

def test_ex_15_09_state_graph_engine():
    g = StateGraphEngine(entry_point="step1")
    g.add_node("step1", lambda s: {"count": s.get("count", 0) + 1})
    g.add_conditional_edge("step1", lambda s: "END" if s["count"] >= 2 else "step1")
    final = g.run({"count": 0})
    assert final["count"] == 2

def test_ex_15_10_save_and_resume_checkpoint():
    store = {}
    restored = save_and_resume_checkpoint({"step": 3}, store, "t1")
    assert restored == {"step": 3} and "t1" in store
