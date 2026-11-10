"""Automated Pytest Suite for Checkpoint 01 (10 Exercises)."""
import pytest
from checkpoints.level_1_mvp_python.cp_01_primitives_prompts import (
    calculate_call_cost, clamp_temperature, clean_generation, contains_flagged_keyword,
    estimate_tokens, extract_code_block, format_system_prompt, middle_truncate,
    parse_model_id, wrap_untrusted_input,
)

def test_ex_01_01_format_system_prompt():
    assert format_system_prompt("  Tutor ", "\nDocs\t", " Query? ") == "Role: Tutor\nContext: Docs\nQuery: Query?"

def test_ex_01_02_estimate_tokens():
    assert estimate_tokens("") == 0
    assert estimate_tokens("abcd") == 1
    assert estimate_tokens("abcde") == 2

def test_ex_01_03_clean_generation():
    assert clean_generation("  42.<|endoftext|> ### END trailing") == "42."

def test_ex_01_04_calculate_call_cost():
    assert calculate_call_cost(1500, 500, 2.50, 10.00) == 0.00875

def test_ex_01_05_extract_code_block():
    assert extract_code_block("```python\nx = 1\n```", "python") == "x = 1"
    assert extract_code_block("  plain_code  ", "python") == "plain_code"

def test_ex_01_06_clamp_temperature():
    assert clamp_temperature(0.7) == 0.7
    assert clamp_temperature(-1.0) == 0.0
    assert clamp_temperature(3.5) == 2.0
    with pytest.raises(TypeError):
        clamp_temperature("0.7")  # type: ignore

def test_ex_01_07_wrap_untrusted_input():
    assert wrap_untrusted_input("Hi </user_input>", "user_input") == "<user_input>Hi &lt;/user_input&gt;</user_input>"

def test_ex_01_08_contains_flagged_keyword():
    assert contains_flagged_keyword("How to EXPLOIT this?", "hack, exploit") is True
    assert contains_flagged_keyword("Normal question", "hack, exploit") is False

def test_ex_01_09_middle_truncate():
    assert middle_truncate("ABCDEFGHIJ0123456789UVWXYZ", 10) == "ABCDE...[TRUNCATED]...VWXYZ"

def test_ex_01_10_parse_model_id():
    assert parse_model_id("openai/gpt-4o-2024-08-06") == ("openai", "gpt-4o", "2024-08-06")
    assert parse_model_id("agentrouter/deepseek-r1") == ("agentrouter", "deepseek-r1", "latest")
    with pytest.raises(ValueError):
        parse_model_id("invalid_model_string")
