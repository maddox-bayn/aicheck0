"""Automated Pytest Suite for Checkpoint 07 (10 Exercises)."""
from pathlib import Path
import pytest
from checkpoints.level_2_conversational_core.cp_07_memory_state_management import (
    BufferWindowMemory, compact_history_with_summary, count_exact_tokens,
    count_messages_tokens, enforce_context_window, fork_conversation,
    load_or_create_session, merge_consecutive_roles, sanitize_message_sequence,
    update_entity_memory,
)

def test_ex_07_01_count_exact_tokens():
    assert count_exact_tokens("Hello world") > 0

def test_ex_07_02_count_messages_tokens():
    assert count_messages_tokens([{"role": "user", "content": "Hello"}]) >= 4

def test_ex_07_03_buffer_window_memory():
    mem = BufferWindowMemory("Sys", k_turns=1)
    mem.add_turn("u1", "a1")
    mem.add_turn("u2", "a2")
    msgs = mem.get_messages()
    assert len(msgs) == 3 and msgs[1]["content"] == "u2"

def test_ex_07_04_enforce_context_window():
    msgs = [{"role": "system", "content": "S"}, {"role": "user", "content": "Old " * 50}, {"role": "user", "content": "New"}]
    res = enforce_context_window(msgs, max_context_tokens=30)
    assert res[0]["role"] == "system" and res[-1]["content"] == "New"

def test_ex_07_05_compact_history_with_summary():
    msgs = [{"role": "system", "content": "S"}, {"role": "user", "content": "1"}, {"role": "assistant", "content": "2"}, {"role": "user", "content": "3"}]
    res = compact_history_with_summary(msgs, threshold=3, summarizer_fn=lambda _: "SummaryText")
    assert any("SummaryText" in m["content"] for m in res)

def test_ex_07_06_load_or_create_session(tmp_path: Path):
    s = load_or_create_session("user_1", str(tmp_path), "SysPrompt")
    assert s == [{"role": "system", "content": "SysPrompt"}]
    with pytest.raises(ValueError):
        load_or_create_session("../hack", str(tmp_path), "Sys")

def test_ex_07_07_update_entity_memory():
    store = {"name": "Maddox"}
    out = update_entity_memory(store, {"lang": "Python"})
    assert "name: Maddox" in out and "lang: Python" in out

def test_ex_07_08_sanitize_message_sequence():
    msgs = [{"role": "system", "content": "S"}, {"role": "assistant", "content": "Orphan"}, {"role": "user", "content": "Hi"}]
    assert sanitize_message_sequence(msgs) == [{"role": "system", "content": "S"}, {"role": "user", "content": "Hi"}]

def test_ex_07_09_fork_conversation():
    msgs = [{"role": "system", "content": "S"}, {"role": "user", "content": "U1"}, {"role": "assistant", "content": "A1"}]
    forked = fork_conversation(msgs, 1, "NewU1")
    assert len(forked) == 2 and forked[1]["content"] == "NewU1"

def test_ex_07_10_merge_consecutive_roles():
    msgs = [{"role": "user", "content": "Part 1"}, {"role": "user", "content": "Part 2"}]
    assert merge_consecutive_roles(msgs) == [{"role": "user", "content": "Part 1\n\nPart 2"}]
