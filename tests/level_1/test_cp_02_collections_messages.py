"""Automated Pytest Suite for Checkpoint 02 (10 Exercises)."""
import pytest
from checkpoints.level_1_mvp_python.cp_02_collections_messages import (
    append_exchange, build_message, build_unique_vocab, count_messages_by_role,
    create_batches, deduplicate_documents, extract_token_usage, format_few_shot_messages,
    merge_metadata, top_k_logprobs,
)

def test_ex_02_01_build_message():
    assert build_message("user", "Hi") == {"role": "user", "content": "Hi"}
    with pytest.raises(ValueError):
        build_message("invalid", "Hi")

def test_ex_02_02_append_exchange():
    orig = [{"role": "system", "content": "Sys"}]
    res = append_exchange(orig, "U", "A")
    assert len(orig) == 1 and len(res) == 3

def test_ex_02_03_build_unique_vocab():
    assert build_unique_vocab(["The", "AI", "Bot", "bot", "runs"], {"the"}) == ["bot", "runs"]

def test_ex_02_04_create_batches():
    assert create_batches(["a", "b", "c"], 2) == [["a", "b"], ["c"]]
    with pytest.raises(ValueError):
        create_batches(["a"], 0)

def test_ex_02_05_count_messages_by_role():
    msgs = [{"role": "user", "content": "1"}, {"role": "assistant", "content": "2"}]
    assert count_messages_by_role(msgs) == {"system": 0, "user": 1, "assistant": 1, "tool": 0}

def test_ex_02_06_top_k_logprobs():
    assert top_k_logprobs({"No": -2.0, "Yes": -0.1, "Maybe": -0.5}, 2) == ["Yes", "Maybe"]

def test_ex_02_07_merge_metadata():
    assert merge_metadata({"a": 1, "b": None}, {"b": 2, "c": None}) == {"a": 1, "b": 2}

def test_ex_02_08_extract_token_usage():
    resp = {"usage": {"prompt_tokens": 10, "completion_tokens": 5, "prompt_tokens_details": {"cached_tokens": 2}}}
    assert extract_token_usage(resp) == (10, 5, 2)
    assert extract_token_usage({}) == (0, 0, 0)

def test_ex_02_09_deduplicate_documents():
    docs = [{"id": "1", "text": "X"}, {"id": "2", "text": "Y"}, {"id": "3", "text": "X"}]
    assert deduplicate_documents(docs) == [{"id": "1", "text": "X"}, {"id": "2", "text": "Y"}]

def test_ex_02_10_format_few_shot_messages():
    assert format_few_shot_messages([("Q", "A")]) == [{"role": "user", "content": "Q"}, {"role": "assistant", "content": "A"}]
