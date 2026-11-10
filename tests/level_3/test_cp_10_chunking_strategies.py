"""Automated Pytest Suite for Checkpoint 10 (10 Exercises)."""
import pytest
from checkpoints.level_3_rag_engine.cp_10_chunking_strategies import (
    chunk_document_with_offsets, chunk_python_code_by_ast, create_parent_child_chunks,
    enrich_chunks_with_headers, merge_short_chunks, recursive_split_text,
    split_by_sentences, split_by_tokens, split_fixed_characters, split_markdown_by_headers,
)

def test_ex_10_01_split_fixed_characters():
    assert split_fixed_characters("0123456789", 4, 2) == ["0123", "2345", "4567", "6789"]
    with pytest.raises(ValueError):
        split_fixed_characters("abc", 4, 4)

def test_ex_10_02_split_by_sentences():
    chunks = split_by_sentences("First sentence. Second sentence! Third?", max_chars=35)
    assert len(chunks) == 2

def test_ex_10_03_recursive_split_text():
    chunks = recursive_split_text("Para 1\n\nPara 2 is longer", chunk_size=10)
    assert all(len(c) <= 10 for c in chunks)

def test_ex_10_04_split_by_tokens():
    chunks = split_by_tokens("w1 w2 w3 w4 w5", max_tokens=3, overlap_tokens=1)
    assert len(chunks) >= 2

def test_ex_10_05_split_markdown_by_headers():
    md = "# H1\nIntro\n## H2\nDetails"
    chunks = split_markdown_by_headers(md)
    assert len(chunks) == 2 and chunks[1]["metadata"]["h2"] == "H2"

def test_ex_10_06_chunk_python_code_by_ast():
    code = "def foo():\n    return 1\n\nclass Bar:\n    pass\n"
    items = chunk_python_code_by_ast(code)
    assert [i["name"] for i in items] == ["foo", "Bar"]

def test_ex_10_07_create_parent_child_chunks():
    parents, children = create_parent_child_chunks("doc1", "A" * 250, parent_size=150, child_size=60)
    assert len(parents) == 2 and all(c["parent_id"] in parents for c in children)

def test_ex_10_08_enrich_chunks_with_headers():
    res = enrich_chunks_with_headers([{"text": "Body", "metadata": {"title": "Doc", "section": "S1"}}])
    assert res == ["[Title: Doc | Section: S1]\nBody"]

def test_ex_10_09_merge_short_chunks():
    assert merge_short_chunks(["Long enough chunk one", "tiny", "Long enough chunk two"], min_chars=10) == [
        "Long enough chunk one tiny", "Long enough chunk two"
    ]

def test_ex_10_10_chunk_document_with_offsets():
    res = chunk_document_with_offsets("0123456789", 4, 1)
    assert res[0]["start_char"] == 0 and res[1]["start_char"] == 3
