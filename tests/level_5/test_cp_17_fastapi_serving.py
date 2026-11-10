"""Automated Pytest Suite for Checkpoint 17 (10 Exercises)."""
import asyncio
from fastapi import HTTPException
from fastapi.testclient import TestClient
import pytest
from checkpoints.level_5_production_eval.cp_17_fastapi_serving import (
    ChatRequest, ChatResponse, SlidingWindowLimiter, build_testable_app,
    check_system_readiness, create_chat_app, create_lifespan_handler,
    log_telemetry_background, map_exception_to_http_response,
    sse_event_generator, verify_api_key,
)

def test_ex_17_01_chat_models():
    req = ChatRequest(session_id="s1", message="Hi")
    resp = ChatResponse(session_id="s1", reply="Hello")
    assert req.temperature == 0.7 and resp.reply == "Hello"

def test_ex_17_02_create_chat_app():
    app = create_chat_app(lambda sid, msg: f"{sid}:{msg}")
    client = TestClient(app)
    r = client.post("/v1/chat", json={"session_id": "s1", "message": "ping"})
    assert r.status_code == 200 and r.json()["reply"] == "s1:ping"

def test_ex_17_03_sse_event_generator():
    async def collect():
        return [chunk async for chunk in sse_event_generator(["Hel", "lo"])]
    events = asyncio.run(collect())
    assert events[-1] == "data: [DONE]\n\n" and len(events) == 3

def test_ex_17_04_build_testable_app():
    app, dep = build_testable_app(lambda: "prod_model")
    app.dependency_overrides[dep] = lambda: "mock_model"
    client = TestClient(app)
    assert client.get("/v1/model-info").json() == {"model": "mock_model"}

def test_ex_17_05_verify_api_key():
    assert verify_api_key("secret1", {"secret1"}) == "secret1"
    with pytest.raises(HTTPException) as exc:
        verify_api_key("wrong", {"secret1"})
    assert exc.value.status_code == 401

def test_ex_17_06_log_telemetry_background():
    audit = []
    log_telemetry_background(audit, "s1", "p", "r", 42)
    assert len(audit) == 1 and audit[0]["tokens"] == 42

def test_ex_17_07_check_system_readiness():
    assert check_system_readiness(lambda: True, lambda: True)[0] == 200
    assert check_system_readiness(lambda: True, lambda: False)[0] == 503

def test_ex_17_08_sliding_window_limiter():
    lim = SlidingWindowLimiter(max_requests=2, window_seconds=60.0)
    assert lim.check_or_raise("u1") is True
    assert lim.check_or_raise("u1") is True
    with pytest.raises(HTTPException) as exc:
        lim.check_or_raise("u1")
    assert exc.value.status_code == 429

def test_ex_17_09_map_exception_to_http_response():
    code, body = map_exception_to_http_response(TimeoutError("slow"))
    assert code == 504 and "slow" in body["detail"]

def test_ex_17_10_create_lifespan_handler():
    state_log = []
    lifespan = create_lifespan_handler(lambda: state_log.append("init") or {}, lambda: state_log.append("clean"))
    async def run_ls():
        async with lifespan(None):
            state_log.append("inside")
    asyncio.run(run_ls())
    assert state_log == ["init", "inside", "clean"]
