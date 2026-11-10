"""Automated Pytest Suite for Checkpoint 13 (10 Exercises)."""
import pytest
from checkpoints.level_4_multi_tool_agent.cp_13_pydantic_schemas import (
    StockLookupArgs, TaskPlan, enforce_strict_json_schema, openai_to_anthropic_tool,
    parse_with_self_correction, pydantic_to_openai_tool, resolve_tool_choice,
    tool, validate_structured_output, validate_ticket_classification,
)

def test_ex_13_01_stock_lookup_args():
    s = StockLookupArgs(ticker=" nvda ", days=30)
    assert s.ticker == "NVDA"
    with pytest.raises(Exception):
        StockLookupArgs(ticker="INVALIDTICKER", days=10)

def test_ex_13_02_pydantic_to_openai_tool():
    t = pydantic_to_openai_tool("lookup", "Lookup stock", StockLookupArgs)
    assert t["type"] == "function" and t["function"]["name"] == "lookup"

def test_ex_13_03_enforce_strict_json_schema():
    raw = {"type": "object", "properties": {"a": {"type": "string"}}}
    strict = enforce_strict_json_schema(raw)
    assert strict["additionalProperties"] is False and strict["required"] == ["a"]

def test_ex_13_04_validate_structured_output():
    inst, err = validate_structured_output('{"ticker": "AAPL", "days": 5}', StockLookupArgs)
    assert inst is not None and err is None
    inst2, err2 = validate_structured_output('{"ticker": "AAPL", "days": 9999}', StockLookupArgs)
    assert inst2 is None and err2 is not None

def test_ex_13_05_parse_with_self_correction():
    responses = iter(['{"ticker": "BAD_123", "days": 5}', '{"ticker": "MSFT", "days": 10}'])
    model = parse_with_self_correction("Get MSFT", StockLookupArgs, lambda _: next(responses))
    assert model.ticker == "MSFT"

def test_ex_13_06_validate_ticket_classification():
    res = validate_ticket_classification({"category": "billing", "urgency": "high", "confidence": 0.95})
    assert res["category"] == "billing"
    with pytest.raises(ValueError):
        validate_ticket_classification({"category": "unknown", "urgency": "low", "confidence": 0.5})

def test_ex_13_07_task_plan():
    p = TaskPlan(goal="Ship", steps=[{"step_id": 1, "task": "A", "depends_on": []}, {"step_id": 2, "task": "B", "depends_on": [1]}])
    assert len(p.steps) == 2
    with pytest.raises(Exception):
        TaskPlan(goal="Bad", steps=[{"step_id": 1, "task": "A", "depends_on": [2]}])

def test_ex_13_08_tool_decorator():
    @tool
    def add_numbers(a: int, b: int) -> int:
        """Add two integers."""
        return a + b
    assert add_numbers(2, 3) == 5 and add_numbers.tool_schema["name"] == "add_numbers"

def test_ex_13_09_openai_to_anthropic_tool():
    oa = {"type": "function", "function": {"name": "calc", "description": "d", "parameters": {"type": "object"}}}
    ant = openai_to_anthropic_tool(oa)
    assert ant == {"name": "calc", "description": "d", "input_schema": {"type": "object"}}

def test_ex_13_10_resolve_tool_choice():
    assert resolve_tool_choice("auto") == "auto"
    assert resolve_tool_choice("get_weather") == {"type": "function", "function": {"name": "get_weather"}}
