"""Automated Pytest Suite for Checkpoint 12 (10 Exercises)."""
from checkpoints.level_3_rag_engine.cp_12_vector_stores_rag import (
    RAGEngine, SimpleVectorStore, build_rag_messages, extract_cited_sources,
    filter_by_min_score, format_rag_context, generate_hyde_embedding,
    match_metadata_filter, rerank_documents, rewrite_conversational_query,
)

def test_ex_12_01_simple_vector_store():
    vs = SimpleVectorStore()
    vs.add_documents([{"text": "A", "meta": {"k": 1}}, {"text": "B", "meta": {"k": 2}}], [[1.0, 0.0], [0.0, 1.0]])
    res = vs.similarity_search([1.0, 0.0], k=1)
    assert res[0][0]["text"] == "A"

def test_ex_12_02_match_metadata_filter():
    assert match_metadata_filter({"dept": "eng", "yr": 2026}, {"dept": "eng", "yr": {"$in": [2025, 2026]}}) is True
    assert match_metadata_filter({"dept": "hr"}, {"dept": "eng"}) is False

def test_ex_12_03_filter_by_min_score():
    assert filter_by_min_score([("d1", 0.8), ("d2", 0.5)], min_score=0.7) == ["d1"]

def test_ex_12_04_format_rag_context():
    ctx = format_rag_context([{"text": "Fact 1", "source": "a.txt"}], max_chars=500)
    assert '<source id="1" file="a.txt">Fact 1</source>' in ctx

def test_ex_12_05_build_rag_messages():
    msgs = build_rag_messages("<source>ctx</source>", "What is X?")
    assert msgs[0]["role"] == "system" and "INSUFFICIENT_CONTEXT" in msgs[0]["content"]

def test_ex_12_06_rewrite_conversational_query():
    q = rewrite_conversational_query([{"role": "user", "content": "Tell me about FastAPI"}], "Is it fast?", lambda p: "Is FastAPI fast?")
    assert q == "Is FastAPI fast?"

def test_ex_12_07_generate_hyde_embedding():
    emb = generate_hyde_embedding("Q", lambda q: "Hypo", lambda t: [float(len(t))])
    assert emb == [float(len("Q\nHypo"))]

def test_ex_12_08_rerank_documents():
    docs = [{"text": "low"}, {"text": "high_match"}]
    ranked = rerank_documents("match", docs, lambda q, d: 1.0 if q in d else 0.1, top_n=1)
    assert ranked[0]["text"] == "high_match"

def test_ex_12_09_extract_cited_sources():
    docs = [{"source": "doc1.pdf"}, {"source": "doc2.pdf"}]
    res = extract_cited_sources("Based on [2] and [1].", docs)
    assert res["sources"] == ["doc2.pdf", "doc1.pdf"]

def test_ex_12_10_rag_engine_milestone():
    eng = RAGEngine(embed_fn=lambda t: [1.0, 0.0] if "python" in t.lower() else [0.0, 1.0], llm_fn=lambda msgs: "Python [1]")
    eng.ingest_text("py.txt", "Python is great for AI.")
    out = eng.answer("Tell me about Python")
    assert "Python" in out["answer"] and out["sources"] == ["py.txt"]
