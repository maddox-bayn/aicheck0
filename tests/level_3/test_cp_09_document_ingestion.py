"""Automated Pytest Suite for Checkpoint 09 (10 Exercises)."""
from pathlib import Path
from checkpoints.level_3_rag_engine.cp_09_document_ingestion import (
    Document, clean_pdf_text, detect_corpus_changes, extract_clean_html_text,
    load_csv_documents, load_directory_corpus, load_pdf_pages, load_text_document,
    parse_markdown_frontmatter, redact_pii,
)

def test_ex_09_01_document_dataclass():
    d = Document(page_content="Hello", metadata={"source": "a.txt"})
    assert d.doc_id and len(d.doc_id) >= 8

def test_ex_09_02_load_text_document(tmp_path: Path):
    p = tmp_path / "doc.txt"
    p.write_text("Hello RAG", encoding="utf-8")
    doc = load_text_document(str(p))
    assert doc.page_content == "Hello RAG" and doc.metadata["char_count"] == 9

def test_ex_09_03_load_pdf_pages():
    docs = load_pdf_pages(["Page 1", "   ", "Page 3"], "book.pdf")
    assert len(docs) == 2 and docs[1].metadata["page"] == 3

def test_ex_09_04_clean_pdf_text():
    assert clean_pdf_text("trans-\nformer   model\n\n\ntest") == "transformer model\n\ntest"

def test_ex_09_05_extract_clean_html_text():
    html = "<html><script>bad()</script><body><nav>Menu</nav><p>Main text</p></body></html>"
    assert extract_clean_html_text(html) == "Main text"

def test_ex_09_06_load_csv_documents(tmp_path: Path):
    p = tmp_path / "items.csv"
    p.write_text("title,body,id\nAI,Great,1\n", encoding="utf-8")
    docs = load_csv_documents(str(p), ["title", "body"], ["id"])
    assert len(docs) == 1 and "title: AI" in docs[0].page_content and docs[0].metadata["id"] == "1"

def test_ex_09_07_load_directory_corpus(tmp_path: Path):
    (tmp_path / "a.txt").write_text("A", encoding="utf-8")
    (tmp_path / ".hidden.txt").write_text("H", encoding="utf-8")
    docs = load_directory_corpus(str(tmp_path))
    assert len(docs) == 1 and docs[0].page_content == "A"

def test_ex_09_08_parse_markdown_frontmatter():
    md = "---\ntitle: Guide\nauthor: Maddox\n---\n# Body"
    body, meta = parse_markdown_frontmatter(md)
    assert body == "# Body" and meta["title"] == "Guide"

def test_ex_09_09_redact_pii():
    out = redact_pii("Email me at test@example.com or 123-45-6789.")
    assert "[REDACTED_EMAIL]" in out and "[REDACTED_SSN]" in out

def test_ex_09_10_detect_corpus_changes():
    d1 = Document("NewContent", {"source": "s1"})
    new_d, upd_d, del_s = detect_corpus_changes([d1], {"s1": "old_hash", "s2": "h2"})
    assert len(new_d) == 0 and len(upd_d) == 1 and del_s == ["s2"]
