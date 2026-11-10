"""Automated Pytest Suite for Checkpoint 05 (10 Exercises)."""
import asyncio
import pytest
from checkpoints.level_2_conversational_core.cp_05_http_rest_fundamentals import (
    build_auth_headers, build_chat_payload, classify_http_status, compute_request_hash,
    fetch_concurrent_completions, normalize_endpoint_url, parse_rate_limit_wait,
    parse_sse_line, post_chat_completion, safe_http_call,
)

def test_ex_05_01_build_auth_headers():
    h = build_auth_headers("key123", org_id="org1")
    assert h["Authorization"] == "Bearer key123" and h["OpenAI-Organization"] == "org1"

def test_ex_05_02_build_chat_payload():
    p = build_chat_payload("gpt-4o", [{"role": "user", "content": "Hi"}], 0.5, 100)
    assert p["model"] == "gpt-4o" and p["max_tokens"] == 100

def test_ex_05_03_post_chat_completion():
    class DummyResp:
        status_code = 200
        def json(self): return {"id": "chatcmpl-1"}
    class DummyClient:
        def post(self, url, headers=None, json=None, timeout=None): return DummyResp()
    assert post_chat_completion("https://api.agentrouter.org/v1/chat/completions", {}, {}, client=DummyClient()) == {"id": "chatcmpl-1"}

def test_ex_05_04_classify_http_status():
    assert classify_http_status(200) == "SUCCESS"
    assert classify_http_status(429) == "RETRYABLE"
    assert classify_http_status(401) == "FATAL"

def test_ex_05_05_parse_rate_limit_wait():
    assert parse_rate_limit_wait({"retry-after": "2.5"}) == 2.5

def test_ex_05_06_parse_sse_line():
    line = 'data: {"choices": [{"delta": {"content": "Hi"}}]}'
    assert parse_sse_line(line) == "Hi"
    assert parse_sse_line("data: [DONE]") is None

def test_ex_05_07_safe_http_call():
    res = safe_http_call(lambda: (_ for _ in ()).throw(TimeoutError("timed out")))
    assert res["retryable"] is True and "timed out" in res["error"]

def test_ex_05_08_fetch_concurrent_completions():
    async def fake_post(url, headers, payload):
        return {"echo": payload["id"]}
    out = asyncio.run(fetch_concurrent_completions("u", {}, [{"id": 1}, {"id": 2}], fake_post))
    assert out == [{"echo": 1}, {"echo": 2}]

def test_ex_05_09_normalize_endpoint_url():
    assert normalize_endpoint_url("https://api.agentrouter.org/v1/") == "https://api.agentrouter.org/v1/chat/completions"

def test_ex_05_10_compute_request_hash():
    h1 = compute_request_hash({"a": 1, "b": 2})
    h2 = compute_request_hash({"b": 2, "a": 1})
    assert h1 == h2 and len(h1) == 64
