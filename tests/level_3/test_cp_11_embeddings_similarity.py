"""Automated Pytest Suite for Checkpoint 11 (10 Exercises)."""
import numpy as np
from checkpoints.level_3_rag_engine.cp_11_embeddings_similarity import (
    compute_bm25_scores, cosine_similarity, embed_texts_in_batches,
    euclidean_top_k, find_semantic_breakpoints, l2_normalize_vectors,
    maximal_marginal_relevance, reciprocal_rank_fusion, truncate_matryoshka_embedding,
    vectorized_top_k,
)

def test_ex_11_01_l2_normalize_vectors():
    v = np.array([[3.0, 4.0], [0.0, 0.0]])
    normed = l2_normalize_vectors(v)
    assert np.allclose(normed[0], [0.6, 0.8]) and np.allclose(normed[1], [0.0, 0.0])

def test_ex_11_02_cosine_similarity():
    assert round(cosine_similarity([1.0, 0.0], [1.0, 0.0]), 4) == 1.0
    assert cosine_similarity([0.0, 0.0], [1.0, 2.0]) == 0.0

def test_ex_11_03_vectorized_top_k():
    q = np.array([1.0, 0.0])
    corpus = np.array([[0.0, 1.0], [1.0, 0.0], [0.7, 0.7]])
    top = vectorized_top_k(q, corpus, k=2)
    assert top[0][0] == 1 and top[1][0] == 2

def test_ex_11_04_euclidean_top_k():
    q = np.array([0.0, 0.0])
    corpus = np.array([[3.0, 4.0], [1.0, 0.0]])
    top = euclidean_top_k(q, corpus, k=1)
    assert top[0][0] == 1 and top[0][1] == 1.0

def test_ex_11_05_embed_texts_in_batches():
    out = embed_texts_in_batches(lambda batch: [[float(len(x))] for x in batch], ["a\nb", "cde", "f"], batch_size=2)
    assert out == [[3.0], [3.0], [1.0]]

def test_ex_11_06_truncate_matryoshka_embedding():
    res = truncate_matryoshka_embedding([3.0, 4.0, 99.0, 100.0], target_dim=2)
    assert np.allclose(res, [0.6, 0.8])

def test_ex_11_07_maximal_marginal_relevance():
    q = np.array([1.0, 0.0])
    docs = np.array([[1.0, 0.0], [0.99, 0.01], [0.5, 0.86]])
    idx = maximal_marginal_relevance(q, docs, k=2, lambda_mult=0.5)
    assert idx[0] == 0 and 2 in idx

def test_ex_11_08_find_semantic_breakpoints():
    embs = np.array([[1.0, 0.0], [0.99, 0.01], [0.0, 1.0], [0.01, 0.99]])
    assert find_semantic_breakpoints(embs, percentile_threshold=60.0) == [1]

def test_ex_11_09_compute_bm25_scores():
    corpus = [["python", "ai", "rag"], ["cooking", "pasta", "recipe"]]
    scores = compute_bm25_scores(["python", "rag"], corpus)
    assert scores[0] > scores[1]

def test_ex_11_10_reciprocal_rank_fusion():
    fused = reciprocal_rank_fusion([["d1", "d2"], ["d2", "d1"]], rrf_k=60)
    assert len(fused) == 2 and fused[0][1] == fused[1][1]
