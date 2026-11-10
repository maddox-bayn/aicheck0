"""Automated Pytest Suite for Checkpoint 04 (10 Exercises)."""
from datetime import datetime
import json
from pathlib import Path
import pytest
from checkpoints.level_1_mvp_python.cp_04_json_env_config import (
    apply_env_overrides, export_transcript_to_md, load_and_validate_config,
    load_api_key, mask_secret, read_jsonl, run_mvp_config_pipeline,
    safe_parse_llm_json, serialize_complex_state, write_jsonl,
)

def test_ex_04_01_safe_parse_llm_json():
    assert safe_parse_llm_json("```json\n{\"k\": 1,}\n```") == {"k": 1}
    assert safe_parse_llm_json("bad", default={"d": 0}) == {"d": 0}

def test_ex_04_02_load_api_key(tmp_path: Path):
    p = tmp_path / ".env"
    p.write_text("AGENTROUTER_API_KEY=ar-1234567890abcdef\n", encoding="utf-8")
    assert load_api_key(str(p), "AGENTROUTER_API_KEY") == "ar-1234567890abcdef"
    with pytest.raises(OSError):
        load_api_key(str(p), "MISSING")

def test_ex_04_03_mask_secret():
    assert mask_secret("ar-1234567890abcdef") == "ar-1...cdef"
    assert mask_secret("short") == "***"

def test_ex_04_04_read_jsonl(tmp_path: Path):
    p = tmp_path / "t.jsonl"
    p.write_text('{"a": 1}\n\n{"b": 2}\n', encoding="utf-8")
    assert read_jsonl(str(p)) == [{"a": 1}, {"b": 2}]

def test_ex_04_05_write_jsonl(tmp_path: Path):
    p = tmp_path / "out.jsonl"
    assert write_jsonl([{"x": 1}], str(p)) == 1
    assert read_jsonl(str(p)) == [{"x": 1}]

def test_ex_04_06_load_and_validate_config(tmp_path: Path):
    p = tmp_path / "c.json"
    cfg = {"model": {"name": "gpt-4o", "temperature": 0.5}, "system_prompt": "Sys"}
    p.write_text(json.dumps(cfg), encoding="utf-8")
    assert load_and_validate_config(str(p)) == cfg

def test_ex_04_07_serialize_complex_state():
    data = json.loads(serialize_complex_state({"dt": datetime(2026, 1, 1, 0, 0), "s": {"b", "a"}}))
    assert data["dt"].startswith("2026-01-01") and data["s"] == ["a", "b"]

def test_ex_04_08_export_transcript_to_md(tmp_path: Path):
    src, dst = tmp_path / "in.json", tmp_path / "out.md"
    src.write_text(json.dumps([{"role": "user", "content": "Hi"}]), encoding="utf-8")
    assert "### User\nHi" in export_transcript_to_md(str(src), str(dst))

def test_ex_04_09_apply_env_overrides(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("AI_MODEL", "deepseek-r1")
    monkeypatch.setenv("AI_TIMEOUT", "45")
    assert apply_env_overrides({"model": "old", "timeout": 10}) == {"model": "deepseek-r1", "timeout": 45}

def test_ex_04_10_run_mvp_config_pipeline(tmp_path: Path):
    p = tmp_path / "cfg.json"
    p.write_text('{"model": "deepseek-chat", "temperature": 0.7}', encoding="utf-8")
    assert run_mvp_config_pipeline(str(p), '{"query": " Hello "}') == "[Model: deepseek-chat | Temp: 0.7] Query: Hello"
