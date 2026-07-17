"""Key-free tests for the public Agentic RAG API."""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

os.environ["AGENTIC_RAG_MODE"] = "stub"
os.environ["EMBEDDING_BACKEND"] = "hash"
os.environ.pop("GROQ_API_KEY", None)
os.environ.pop("TAVILY_API_KEY", None)

from rag_agent import AgenticRAGService, Settings


def build_service() -> AgenticRAGService:
    """Create a fresh deterministic service."""

    return AgenticRAGService(
        Settings(
            mode="stub",
            embedding_backend="hash",
        )
    )


def test_internal_question_uses_kb_and_citations():
    service = build_service()

    result = service.ask(
        "How should a RAG system cite retrieved evidence?"
    )

    assert result["mode"] == "stub"
    assert result["route"] == "kb"
    assert result["sources"]
    assert "[kb:" in result["answer"]
    assert result["tool_calls"][0]["name"] == "search_knowledge_base"


def test_current_question_can_use_web():
    service = build_service()

    result = service.ask(
        "What are the latest LangChain agent changes?"
    )

    assert "web" in result["route"]
    assert any(
        source["origin"] == "mock_web"
        for source in result["sources"]
    )
    assert any(
        call["name"] == "search_web"
        for call in result["tool_calls"]
    )


def test_empty_question_is_handled():
    service = build_service()

    result = service.ask("   ")

    assert result["route"] == "none"
    assert result["sources"] == []
    assert "non-empty" in result["answer"]
