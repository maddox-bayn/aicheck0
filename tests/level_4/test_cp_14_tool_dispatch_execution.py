"""Automated Pytest Suite for Checkpoint 14 (10 Exercises)."""
from pathlib import Path
import sqlite3
import time
import pytest
from checkpoints.level_4_multi_tool_agent.cp_14_tool_dispatch_execution import (
    ToolRegistry, cap_tool_output, check_duplicate_tool_call, execute_parallel_tool_calls,
    execute_readonly_sql, execute_tool_with_timeout, extract_tool_calls,
    format_tool_response_message, handle_unknown_tool, safe_calculator_tool,
)

def test_ex_14_01_tool_registry():
    reg = ToolRegistry()
    reg.register("double", lambda x: x * 2, {"name": "double"})
    assert reg.execute("double", '{"x": 21}') == "42"

def test_ex_14_02_extract_tool_calls():
    msg = {"role": "assistant", "tool_calls": [{"id": "c1", "function": {"name": "f", "arguments": '{"a": 1}'}}]}
    assert extract_tool_calls(msg) == [{"id": "c1", "name": "f", "arguments": {"a": 1}}]

def test_ex_14_03_format_tool_response_message():
    m = format_tool_response_message("c1", "weather", {"temp": 25})
    assert m["role"] == "tool" and m["tool_call_id"] == "c1" and '"temp": 25' in m["content"]

def test_ex_14_04_handle_unknown_tool():
    m = handle_unknown_tool("c1", "bad_fn", ["good_fn"])
    assert m["role"] == "tool" and "good_fn" in m["content"]

def test_ex_14_05_safe_calculator_tool():
    assert safe_calculator_tool("2 ** 3 + sqrt(16)") == 12.0
    with pytest.raises(ValueError):
        safe_calculator_tool("__import__('os').system('ls')")

def test_ex_14_06_execute_parallel_tool_calls():
    reg = ToolRegistry()
    reg.register("add", lambda a, b: a + b)
    calls = [{"id": "1", "name": "add", "arguments": {"a": 1, "b": 2}}, {"id": "2", "name": "add", "arguments": {"a": 3, "b": 4}}]
    res = execute_parallel_tool_calls(calls, reg)
    assert [r["content"] for r in res] == ["3", "7"]

def test_ex_14_07_execute_tool_with_timeout():
    def slow():
        time.sleep(0.2)
        return "done"
    assert "timed out" in execute_tool_with_timeout(slow, {}, timeout_sec=0.05)

def test_ex_14_08_cap_tool_output():
    assert cap_tool_output("0123456789", max_chars=5) == "01234...[TRUNCATED]"

def test_ex_14_09_execute_readonly_sql(tmp_path: Path):
    db = tmp_path / "test.db"
    conn = sqlite3.connect(str(db))
    conn.execute("CREATE TABLE users (id INT, name TEXT)")
    conn.execute("INSERT INTO users VALUES (1, 'Maddox')")
    conn.commit()
    conn.close()
    assert execute_readonly_sql(str(db), "SELECT id, name FROM users") == [{"id": 1, "name": "Maddox"}]
    with pytest.raises(PermissionError):
        execute_readonly_sql(str(db), "DROP TABLE users")

def test_ex_14_10_check_duplicate_tool_call():
    hist = [("search", '{"q":"a"}'), ("search", '{"q":"a"}')]
    assert check_duplicate_tool_call(hist, "search", '{"q":"a"}', max_repeats=2) is True
