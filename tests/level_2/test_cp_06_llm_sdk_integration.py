"""Automated Pytest Suite for Checkpoint 06 (10 Exercises)."""
import pytest
from checkpoints.level_2_conversational_core.cp_06_llm_sdk_integration import (
    UsageTracker, build_vision_message, call_with_sdk_error_handling, create_llm_client,
    deterministic_generate, generate_json_object, generate_text, generate_without_tokens,
    sample_best_candidate, stream_completion,
)

class MockMsg:
    def __init__(self, content): self.content = content

class MockChoice:
    def __init__(self, content):
        self.message = MockMsg(content)
        self.delta = MockMsg(content)

class MockResp:
    def __init__(self, texts, fp="fp_123"):
        self.choices = [MockChoice(t) for t in texts]
        self.system_fingerprint = fp

class MockCompletions:
    def __init__(self): self.last_kwargs = {}
    def create(self, **kwargs):
        self.last_kwargs = kwargs
        if kwargs.get("stream"):
            return [MockResp(["Hello "]), MockResp(["World"])]
        if kwargs.get("n", 1) > 1:
            return MockResp(["As an AI, I cannot", "Short valid", "A much longer valid answer"])
        if kwargs.get("response_format") == {"type": "json_object"}:
            return MockResp(['{"ok": true}'])
        return MockResp(["Mock reply"])

class MockClient:
    def __init__(self):
        self.chat = type("Chat", (), {"completions": MockCompletions()})()

def test_ex_06_01_create_llm_client():
    c = create_llm_client("ar-key", base_url="https://api.agentrouter.org/v1")
    assert c is not None

def test_ex_06_02_generate_text():
    assert generate_text(MockClient(), "gpt-4o", "sys", "user") == "Mock reply"

def test_ex_06_03_stream_completion():
    collected = []
    full = stream_completion(MockClient(), "gpt-4o", [], collected.append)
    assert full == "Hello World" and collected == ["Hello ", "World"]

def test_ex_06_04_generate_json_object():
    assert generate_json_object(MockClient(), "gpt-4o", "Return JSON", "hi") == {"ok": True}
    with pytest.raises(ValueError):
        generate_json_object(MockClient(), "gpt-4o", "No keyword here", "hi")

def test_ex_06_05_sample_best_candidate():
    assert sample_best_candidate(MockClient(), "gpt-4o", "prompt", n=3) == "Short valid"

def test_ex_06_06_deterministic_generate():
    text, fp = deterministic_generate(MockClient(), "gpt-4o", "hi", seed=99)
    assert text == "Mock reply" and fp == "fp_123"

def test_ex_06_07_generate_without_tokens():
    mc = MockClient()
    generate_without_tokens(mc, "gpt-4o", "hi", [101, 202])
    assert mc.chat.completions.last_kwargs["logit_bias"] == {"101": -100, "202": -100}

def test_ex_06_08_build_vision_message():
    msg = build_vision_message("Describe", b"1234", "image/png")
    assert msg["role"] == "user" and isinstance(msg["content"], list)

def test_ex_06_09_call_with_sdk_error_handling():
    assert call_with_sdk_error_handling(lambda: "ok") == {"status": "ok", "data": "ok"}
    err = call_with_sdk_error_handling(lambda: (_ for _ in ()).throw(ValueError("bad")))
    assert err["status"] == "error" and err["type"] == "ValueError"

def test_ex_06_10_usage_tracker():
    ut = UsageTracker()
    ut.record(1000, 500)
    s = ut.summary(2.0, 4.0)
    assert s["prompt_tokens"] == 1000 and s["completion_tokens"] == 500
