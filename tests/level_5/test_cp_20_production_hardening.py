"""Automated Pytest Suite for Checkpoint 20 (10 Exercises)."""
import asyncio
import pytest
from checkpoints.level_5_production_eval.cp_20_production_hardening import (
    ProductionAISystem, PromptRegistry, SemanticCache, TenantQuotaManager,
    assign_prompt_variant, cascade_model_call, execute_with_graceful_degradation,
    order_messages_for_kv_cache, replay_dead_letter_queue, run_bounded_batch,
)

def test_ex_20_01_semantic_cache():
    sc = SemanticCache(similarity_threshold=0.9)
    sc.store([1.0, 0.0], "CachedAnswer")
    assert sc.lookup([0.99, 0.01]) == "CachedAnswer"
    assert sc.lookup([0.0, 1.0]) is None

def test_ex_20_02_cascade_model_call():
    res = cascade_model_call(
        "Hard math",
        small_llm_fn=lambda _: {"answer": "unsure", "confidence": 0.4},
        large_llm_fn=lambda _: {"answer": "42", "confidence": 0.99},
        confidence_threshold=0.8,
    )
    assert res["answer"] == "42" and res["routed_to"] == "large"

def test_ex_20_03_assign_prompt_variant():
    v1 = assign_prompt_variant("user_123", "exp_1", traffic_split_b=0.5)
    v2 = assign_prompt_variant("user_123", "exp_1", traffic_split_b=0.5)
    assert v1 in {"A", "B"} and v1 == v2

def test_ex_20_04_run_bounded_batch():
    async def worker(p: str) -> str:
        await asyncio.sleep(0.01)
        return f"out:{p}"
    res = asyncio.run(run_bounded_batch(["p1", "p2", "p3"], worker, max_concurrency=2))
    assert res == ["out:p1", "out:p2", "out:p3"]

def test_ex_20_05_order_messages_for_kv_cache():
    msgs = order_messages_for_kv_cache("Sys", "StaticDocs", [{"role": "user", "content": "FS"}], [{"role": "user", "content": "Hist"}], "Now?")
    assert msgs[0]["role"] == "system" and "StaticDocs" in msgs[0]["content"] and msgs[-1]["content"] == "Now?"

def test_ex_20_06_execute_with_graceful_degradation():
    bad = lambda _: (_ for _ in ()).throw(RuntimeError("down"))
    res = execute_with_graceful_degradation("reset password", bad, bad, {"password": "Go to settings to reset."})
    assert res["degraded"] is True and "settings" in res["reply"]

def test_ex_20_07_replay_dead_letter_queue():
    dlq = [{"id": 1, "payload": "ok"}, {"id": 2, "payload": "fail"}]
    ok, failed = replay_dead_letter_queue(dlq, lambda item: item["payload"] if item["payload"] == "ok" else (_ for _ in ()).throw(ValueError()))
    assert len(ok) == 1 and len(failed) == 1

def test_ex_20_08_prompt_registry():
    reg = PromptRegistry()
    reg.register("greet", "1.0.0", "Hello {name}!")
    assert reg.render("greet", "1.0.0", name="Maddox") == "Hello Maddox!"

def test_ex_20_09_tenant_quota_manager():
    qm = TenantQuotaManager(budgets={"t1": 1.0})
    assert qm.record_and_check("t1", 0.6) is True
    with pytest.raises(PermissionError, match="Quota Exceeded"):
        qm.record_and_check("t1", 0.6)

def test_ex_20_10_production_ai_system_milestone():
    sys_engine = ProductionAISystem(agent_fn=lambda q: f"Solved:{q}")
    r1 = sys_engine.handle_request({"session_id": "s1", "message": "What is AI?"})
    assert r1["reply"] == "Solved:What is AI?" and r1["cached"] is False
    r2 = sys_engine.handle_request({"session_id": "s1", "message": "What is AI?"})
    assert r2["cached"] is True
    eval_rep = sys_engine.run_production_eval([{"query": "test", "expected": "Solved:test"}])
    assert eval_rep["pass_rate"] == 1.0
