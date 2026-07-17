"""Reusable Agentic RAG service for the Streamlit application.

The module supports two modes:

- real:
  Groq provides the tool-calling model and Tavily provides live web search.
- stub:
  A deterministic planner uses the same vector index and local mock web
  records. This mode needs no API key and is suitable for testing.

`AGENTIC_RAG_MODE=auto` selects real mode only when both GROQ_API_KEY and
TAVILY_API_KEY are present.

The public API is intentionally small:

    service = get_service()
    result = service.ask("How should a RAG system cite evidence?")

The returned dictionary always contains:
    answer, sources, route, tool_calls, mode, warnings
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeout
from dataclasses import asdict, dataclass
from functools import lru_cache
from typing import Any, Iterable, Sequence

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.messages import AIMessage, BaseMessage, ToolMessage
from langchain_core.tools import BaseTool, tool
from langchain_community.vectorstores import FAISS

load_dotenv()


# -------------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------------

@dataclass(frozen=True)
class Settings:
    """Environment-backed runtime settings."""

    mode: str = "auto"
    groq_model: str = "openai/gpt-oss-20b"
    embedding_backend: str = "hash"
    hf_embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    agent_timeout_seconds: int = 60
    tool_timeout_seconds: int = 20

    @classmethod
    def from_env(cls) -> "Settings":
        """Build validated settings from environment variables."""

        mode = os.getenv("AGENTIC_RAG_MODE", "auto").strip().lower()

        if mode not in {"auto", "real", "stub"}:
            raise ValueError(
                "AGENTIC_RAG_MODE must be 'auto', 'real', or 'stub'."
            )

        embedding_backend = os.getenv(
            "EMBEDDING_BACKEND",
            "hash",
        ).strip().lower()

        if embedding_backend not in {"hash", "huggingface"}:
            raise ValueError(
                "EMBEDDING_BACKEND must be 'hash' or 'huggingface'."
            )

        return cls(
            mode=mode,
            groq_model=os.getenv(
                "GROQ_MODEL",
                "openai/gpt-oss-20b",
            ).strip(),
            embedding_backend=embedding_backend,
            hf_embedding_model=os.getenv(
                "HF_EMBEDDING_MODEL",
                "sentence-transformers/all-MiniLM-L6-v2",
            ).strip(),
            agent_timeout_seconds=_positive_int(
                os.getenv("AGENT_TIMEOUT_SECONDS"),
                default=60,
            ),
            tool_timeout_seconds=_positive_int(
                os.getenv("TOOL_TIMEOUT_SECONDS"),
                default=20,
            ),
        )


def _positive_int(value: str | None, default: int) -> int:
    """Parse a positive integer and fall back safely."""

    try:
        parsed = int(value or "")
    except ValueError:
        return default

    return parsed if parsed > 0 else default


def run_with_timeout(callable_, seconds: int, message: str):
    """Execute a blocking callable with a best-effort wall-clock timeout.

    The executor is shut down with ``wait=False`` so the caller can recover
    promptly even when an upstream HTTP client ignores cancellation.
    """

    executor = ThreadPoolExecutor(max_workers=1)
    future = executor.submit(callable_)

    try:
        return future.result(timeout=seconds)
    except FutureTimeout as error:
        future.cancel()
        raise TimeoutError(message) from error
    finally:
        executor.shutdown(wait=False, cancel_futures=True)


def configure_langsmith() -> dict[str, Any]:
    """Configure modern and legacy LangSmith environment aliases.

    LangSmith documents LANGSMITH_* names, while many course materials still
    use LANGCHAIN_* aliases. Supporting both keeps the exercise compatible
    without exposing secret values.
    """

    api_key = (
        os.getenv("LANGSMITH_API_KEY")
        or os.getenv("LANGCHAIN_API_KEY")
        or ""
    ).strip()

    requested = (
        os.getenv("LANGSMITH_TRACING")
        or os.getenv("LANGCHAIN_TRACING_V2")
        or "false"
    ).strip().lower() == "true"

    enabled = bool(api_key and requested)

    endpoint = (
        os.getenv("LANGSMITH_ENDPOINT")
        or os.getenv("LANGCHAIN_ENDPOINT")
        or "https://api.smith.langchain.com"
    )

    project = (
        os.getenv("LANGSMITH_PROJECT")
        or os.getenv("LANGCHAIN_PROJECT")
        or "agentic-rag-streamlit"
    )

    os.environ["LANGSMITH_TRACING"] = str(enabled).lower()
    os.environ["LANGCHAIN_TRACING_V2"] = str(enabled).lower()
    os.environ["LANGSMITH_ENDPOINT"] = endpoint
    os.environ["LANGCHAIN_ENDPOINT"] = endpoint
    os.environ["LANGSMITH_PROJECT"] = project
    os.environ["LANGCHAIN_PROJECT"] = project

    if api_key:
        os.environ.setdefault("LANGSMITH_API_KEY", api_key)
        os.environ.setdefault("LANGCHAIN_API_KEY", api_key)

    return {
        "enabled": enabled,
        "project": project,
        "endpoint": endpoint,
        "api_key_present": bool(api_key),
    }


# -------------------------------------------------------------------------
# Knowledge base and embeddings
# -------------------------------------------------------------------------

KNOWLEDGE_BASE = [
    Document(
        page_content=(
            "Retrieval-Augmented Generation combines retrieved evidence "
            "with model generation. The retriever supplies context, while "
            "the model synthesizes an answer grounded in that context."
        ),
        metadata={
            "source": "kb:rag-basics",
            "title": "RAG fundamentals",
            "topics": ["rag", "retrieval", "generation", "grounding"],
        },
    ),
    Document(
        page_content=(
            "An agentic RAG loop can decide whether to search an internal "
            "index, call an external web-search tool, inspect results, and "
            "repeat before producing a final answer."
        ),
        metadata={
            "source": "kb:agentic-loop",
            "title": "Agentic RAG loop",
            "topics": ["agentic", "agent", "tool", "planner", "loop"],
        },
    ),
    Document(
        page_content=(
            "Grounded answers should place citations near the claims they "
            "support. Source identifiers must come from retrieved records "
            "rather than being invented by the language model."
        ),
        metadata={
            "source": "kb:citations",
            "title": "Citation discipline",
            "topics": ["citation", "source", "grounded", "evidence"],
        },
    ),
    Document(
        page_content=(
            "When retrieval evidence is weak or missing, the assistant "
            "should say so, avoid unsupported claims, and suggest a more "
            "specific follow-up question or a web search."
        ),
        metadata={
            "source": "kb:missing-evidence",
            "title": "Missing evidence policy",
            "topics": ["missing", "weak", "evidence", "follow-up"],
        },
    ),
    Document(
        page_content=(
            "FAISS is a local vector-similarity library. LangChain can "
            "store Document objects in a FAISS index and expose the index "
            "through a retriever interface."
        ),
        metadata={
            "source": "kb:faiss",
            "title": "FAISS vector index",
            "topics": ["faiss", "vector", "index", "retriever"],
        },
    ),
    Document(
        page_content=(
            "LangSmith tracing records model, tool, and chain runs when "
            "tracing is enabled and a valid API key is configured. Secrets "
            "should never be displayed in the application interface."
        ),
        metadata={
            "source": "kb:langsmith",
            "title": "LangSmith tracing",
            "topics": ["langsmith", "trace", "observability", "logging"],
        },
    ),
    Document(
        page_content=(
            "A Streamlit form batches user-entered widget values and sends "
            "them to the Python app when the form submit button is pressed."
        ),
        metadata={
            "source": "kb:streamlit-form",
            "title": "Streamlit forms",
            "topics": ["streamlit", "form", "submit", "interface"],
        },
    ),
]

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "can",
    "do", "does", "for", "from", "how", "i", "in", "is", "it",
    "of", "on", "or", "the", "this", "to", "what", "when",
    "where", "which", "who", "why", "with",
}


def tokenize(text: str) -> set[str]:
    """Return normalized terms for transparent lexical checks."""

    return {
        token
        for token in re.findall(
            r"[a-z0-9]+(?:-[a-z0-9]+)?",
            text.lower(),
        )
        if token not in STOPWORDS and len(token) > 1
    }


class HashEmbeddings(Embeddings):
    """Deterministic, download-free hashing embeddings.

    This is not a semantic foundation model. It creates a reproducible local
    vector index for the assignment and works especially well when query and
    document terminology overlaps.
    """

    def __init__(self, dimensions: int = 384):
        if dimensions < 64:
            raise ValueError("dimensions must be at least 64.")

        self.dimensions = dimensions

    def _embed(self, text: str) -> list[float]:
        vector = [0.0] * self.dimensions

        for token in tokenize(text):
            digest = hashlib.blake2b(
                token.encode("utf-8"),
                digest_size=16,
            ).digest()

            index = int.from_bytes(digest[:8], "big") % self.dimensions
            sign = 1.0 if digest[8] % 2 == 0 else -1.0
            vector[index] += sign

        norm = math.sqrt(sum(value * value for value in vector))

        if norm == 0:
            return vector

        return [value / norm for value in vector]

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Embed a batch of document strings."""

        return [self._embed(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        """Embed one query string."""

        return self._embed(text)


def build_embeddings(settings: Settings) -> Embeddings:
    """Create deterministic or Hugging Face embeddings."""

    if settings.embedding_backend == "huggingface":
        from langchain_huggingface import HuggingFaceEmbeddings

        return HuggingFaceEmbeddings(
            model_name=settings.hf_embedding_model,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

    return HashEmbeddings(dimensions=384)


# -------------------------------------------------------------------------
# Result records
# -------------------------------------------------------------------------

@dataclass(frozen=True)
class SourceRecord:
    """One source shown to the user."""

    citation: str
    title: str
    url: str | None
    snippet: str
    origin: str
    score: float | None = None


@dataclass
class AgentResult:
    """Stable public response returned by the service."""

    answer: str
    sources: list[dict[str, Any]]
    route: str
    tool_calls: list[dict[str, Any]]
    mode: str
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""

        return asdict(self)


# -------------------------------------------------------------------------
# Service
# -------------------------------------------------------------------------

class AgenticRAGService:
    """Own the vector index, tools, model, and answer API."""

    def __init__(self, settings: Settings | None = None):
        self.settings = settings or Settings.from_env()
        self.tracing = configure_langsmith()
        self.warnings: list[str] = []

        self.embeddings = build_embeddings(self.settings)
        self.vector_store = FAISS.from_documents(
            KNOWLEDGE_BASE,
            self.embeddings,
        )

        self.mode = self._resolve_mode()
        self.tools = self._build_tools()
        self.agent = self._build_real_agent() if self.mode == "real" else None

    def _resolve_mode(self) -> str:
        """Choose real or stub mode without exposing key values."""

        has_groq = bool(os.getenv("GROQ_API_KEY", "").strip())
        has_tavily = bool(os.getenv("TAVILY_API_KEY", "").strip())

        if self.settings.mode == "stub":
            return "stub"

        if self.settings.mode == "real":
            if not has_groq or not has_tavily:
                missing = [
                    name
                    for name, present in [
                        ("GROQ_API_KEY", has_groq),
                        ("TAVILY_API_KEY", has_tavily),
                    ]
                    if not present
                ]
                raise RuntimeError(
                    "Real mode requires: " + ", ".join(missing)
                )

            return "real"

        if has_groq and has_tavily:
            return "real"

        self.warnings.append(
            "Real API keys were not both available; deterministic stub "
            "mode was selected."
        )
        return "stub"

    def retrieve_kb(
        self,
        query: str,
        k: int = 3,
    ) -> list[SourceRecord]:
        """Retrieve and lexically rerank internal documents."""

        query = query.strip()

        if not query:
            return []

        candidates = self.vector_store.similarity_search(
            query,
            k=min(max(k * 2, k), len(KNOWLEDGE_BASE)),
        )

        query_terms = tokenize(query)
        ranked = []

        for document in candidates:
            topics = set(document.metadata.get("topics", []))
            overlap = len(
                query_terms
                & (tokenize(document.page_content) | topics)
            )

            ranked.append((overlap, document))

        ranked.sort(key=lambda item: item[0], reverse=True)

        records = []

        for overlap, document in ranked[:k]:
            records.append(
                SourceRecord(
                    citation=document.metadata["source"],
                    title=document.metadata["title"],
                    url=None,
                    snippet=document.page_content,
                    origin="knowledge_base",
                    score=float(overlap),
                )
            )

        return records

    def _mock_web_search(
        self,
        query: str,
        max_results: int = 3,
    ) -> list[SourceRecord]:
        """Return deterministic public-looking records in stub mode."""

        del query

        records = [
            SourceRecord(
                citation="web:langchain-agents",
                title="LangChain agents",
                url="https://docs.langchain.com/oss/python/langchain/agents",
                snippet=(
                    "LangChain agents combine models with tools and run in "
                    "a loop until the model produces a final response."
                ),
                origin="mock_web",
                score=None,
            ),
            SourceRecord(
                citation="web:tavily-langchain",
                title="Tavily LangChain integration",
                url="https://docs.tavily.com/documentation/integrations/langchain",
                snippet=(
                    "The official langchain-tavily package exposes Tavily "
                    "search as a LangChain tool."
                ),
                origin="mock_web",
                score=None,
            ),
            SourceRecord(
                citation="web:groq-models",
                title="Groq supported models",
                url="https://console.groq.com/docs/models",
                snippet=(
                    "Groq publishes active model identifiers and separates "
                    "production models from preview models."
                ),
                origin="mock_web",
                score=None,
            ),
        ]

        return records[:max_results]

    def search_web(
        self,
        query: str,
        max_results: int = 3,
    ) -> list[SourceRecord]:
        """Search Tavily with a timeout, or use deterministic mock records."""

        if self.mode == "stub":
            return self._mock_web_search(query, max_results)

        from langchain_tavily import TavilySearch

        tavily = TavilySearch(
            max_results=max_results,
            topic="general",
            search_depth="basic",
            include_answer=False,
            include_raw_content=False,
        )

        payload = run_with_timeout(
            lambda: tavily.invoke({"query": query}),
            seconds=self.settings.tool_timeout_seconds,
            message="Tavily search exceeded the configured timeout.",
        )

        raw_results = (
            payload.get("results", [])
            if isinstance(payload, dict)
            else payload
        )

        records = []

        for index, item in enumerate(raw_results[:max_results], start=1):
            records.append(
                SourceRecord(
                    citation=f"web:{index}",
                    title=str(item.get("title") or "Untitled result"),
                    url=str(item.get("url") or ""),
                    snippet=str(
                        item.get("content")
                        or item.get("snippet")
                        or ""
                    ),
                    origin="tavily",
                    score=(
                        float(item["score"])
                        if item.get("score") is not None
                        else None
                    ),
                )
            )

        return records

    @staticmethod
    def _records_json(records: Sequence[SourceRecord]) -> str:
        """Serialize source records for LangChain tool messages."""

        return json.dumps(
            [asdict(record) for record in records],
            ensure_ascii=False,
        )

    def _build_tools(self) -> list[BaseTool]:
        """Create tools that close over this service instance."""

        @tool
        def search_knowledge_base(
            query: str,
            k: int = 3,
        ) -> str:
            """Search the internal vector index.

            Use this first for questions about RAG, agents, citations,
            FAISS, LangSmith, or the Streamlit application.
            """

            if not 1 <= k <= 5:
                raise ValueError("k must be between 1 and 5.")

            return self._records_json(
                self.retrieve_kb(query, k=k)
            )

        @tool
        def search_web(
            query: str,
            max_results: int = 3,
        ) -> str:
            """Search the public web for current or external information.

            Use this when the internal knowledge base is insufficient or
            when the question asks about recent information.
            """

            if not 1 <= max_results <= 5:
                raise ValueError(
                    "max_results must be between 1 and 5."
                )

            return self._records_json(
                self.search_web(query, max_results=max_results)
            )

        return [search_knowledge_base, search_web]

    def _build_real_agent(self):
        """Create the current LangChain v1 agent backed by Groq."""

        from langchain_groq import ChatGroq

        model = ChatGroq(
            model=self.settings.groq_model,
            temperature=0,
            timeout=self.settings.agent_timeout_seconds,
            max_retries=2,
        )

        system_prompt = (
            "You are an evidence-aware Agentic RAG assistant. "
            "For every question, call search_knowledge_base first. "
            "Call search_web when the question is current, external, or "
            "the KB evidence is weak. Use only tool evidence. Cite claims "
            "with the exact citation field from tool results, such as "
            "[kb:rag-basics] or [web:1]. Never invent citations. "
            "When evidence is insufficient, say so and suggest a focused "
            "follow-up query. Keep the answer concise."
        )

        return create_agent(
            model=model,
            tools=self.tools,
            system_prompt=system_prompt,
        )

    @staticmethod
    def _message_text(message: BaseMessage) -> str:
        """Extract readable text from a LangChain message."""

        content = getattr(message, "content", "")

        if isinstance(content, str):
            return content

        if isinstance(content, list):
            parts = []

            for block in content:
                if isinstance(block, dict):
                    text = block.get("text")
                    if text:
                        parts.append(str(text))
                elif block:
                    parts.append(str(block))

            return "\n".join(parts)

        return str(content or "")

    @staticmethod
    def _parse_tool_sources(
        messages: Iterable[BaseMessage],
    ) -> list[SourceRecord]:
        """Parse JSON source records returned by tool messages."""

        records: list[SourceRecord] = []
        seen: set[str] = set()

        for message in messages:
            if not isinstance(message, ToolMessage):
                continue

            content = AgenticRAGService._message_text(message)

            try:
                payload = json.loads(content)
            except (TypeError, json.JSONDecodeError):
                continue

            if not isinstance(payload, list):
                continue

            for item in payload:
                if not isinstance(item, dict):
                    continue

                citation = str(item.get("citation") or "").strip()

                if not citation or citation in seen:
                    continue

                seen.add(citation)

                records.append(
                    SourceRecord(
                        citation=citation,
                        title=str(item.get("title") or citation),
                        url=(
                            str(item["url"])
                            if item.get("url")
                            else None
                        ),
                        snippet=str(item.get("snippet") or ""),
                        origin=str(item.get("origin") or "tool"),
                        score=(
                            float(item["score"])
                            if item.get("score") is not None
                            else None
                        ),
                    )
                )

        return records

    @staticmethod
    def _parse_tool_calls(
        messages: Iterable[BaseMessage],
    ) -> list[dict[str, Any]]:
        """Extract model-requested tool calls for UI diagnostics."""

        calls = []

        for message in messages:
            if not isinstance(message, AIMessage):
                continue

            for call in getattr(message, "tool_calls", []) or []:
                calls.append(
                    {
                        "name": call.get("name"),
                        "args": call.get("args", {}),
                        "id": call.get("id"),
                    }
                )

        return calls

    @staticmethod
    def _best_sentence(
        query: str,
        snippet: str,
    ) -> str:
        """Choose a short sentence with the strongest lexical overlap."""

        sentences = [
            sentence.strip()
            for sentence in re.split(
                r"(?<=[.!?])\s+",
                snippet.strip(),
            )
            if sentence.strip()
        ]

        if not sentences:
            return snippet.strip()

        query_terms = tokenize(query)

        return max(
            sentences,
            key=lambda sentence: len(
                query_terms & tokenize(sentence)
            ),
        )

    def _stub_answer(self, question: str) -> AgentResult:
        """Run a transparent planner over the same retrieval components."""

        kb_records = self.retrieve_kb(question, k=3)
        best_kb_score = max(
            (record.score or 0.0 for record in kb_records),
            default=0.0,
        )

        current_terms = {
            "current", "today", "latest", "recent", "news",
            "new", "updated", "version", "release",
        }

        needs_web = bool(
            tokenize(question) & current_terms
        ) or best_kb_score == 0

        web_records = (
            self.search_web(question, max_results=3)
            if needs_web
            else []
        )

        relevant_kb_records = [
            record
            for record in kb_records
            if (record.score or 0.0) > 0
        ]

        sources = [
            *relevant_kb_records,
            *web_records,
        ]

        route = (
            "kb+web"
            if relevant_kb_records and web_records
            else "web"
            if web_records
            else "kb"
        )

        tool_calls = [
            {
                "name": "search_knowledge_base",
                "args": {"query": question, "k": 3},
                "id": "stub-kb-call",
            }
        ]

        if needs_web:
            tool_calls.append(
                {
                    "name": "search_web",
                    "args": {
                        "query": question,
                        "max_results": 3,
                    },
                    "id": "stub-web-call",
                }
            )

        if not sources:
            answer = (
                "The available sources do not contain enough evidence to "
                "answer reliably. Try a more specific question or enable "
                "real Tavily search."
            )
        else:
            statements = []

            for source in sources[:3]:
                sentence = self._best_sentence(
                    question,
                    source.snippet,
                )

                if sentence:
                    statements.append(
                        f"{sentence} [{source.citation}]"
                    )

            answer = " ".join(statements)

            if best_kb_score == 0:
                answer += (
                    " Internal evidence was weak, so external search was "
                    "used; verify time-sensitive claims at the linked sources."
                )

        return AgentResult(
            answer=answer,
            sources=[asdict(record) for record in sources],
            route=route,
            tool_calls=tool_calls,
            mode="stub",
            warnings=list(self.warnings),
        )

    def _real_answer(self, question: str) -> AgentResult:
        """Invoke the LangChain agent and inspect its complete message trace."""

        if self.agent is None:
            raise RuntimeError("The real agent has not been initialized.")

        state = run_with_timeout(
            lambda: self.agent.invoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": question,
                        }
                    ]
                },
                {
                    "run_name": "agentic_rag_question",
                    "tags": ["streamlit", "agentic-rag"],
                    "metadata": {
                        "mode": "real",
                        "embedding_backend": (
                            self.settings.embedding_backend
                        ),
                    },
                },
            ),
            seconds=self.settings.agent_timeout_seconds,
            message="The agent exceeded the configured timeout.",
        )

        messages = state.get("messages", [])
        sources = self._parse_tool_sources(messages)
        calls = self._parse_tool_calls(messages)

        final_text = ""

        for message in reversed(messages):
            if isinstance(message, AIMessage):
                text = self._message_text(message).strip()

                if text and not getattr(message, "tool_calls", None):
                    final_text = text
                    break

        if not final_text:
            final_text = (
                "The agent completed without a readable final response."
            )

        # Add an auditable source list if the model omitted inline citations.
        if sources and not any(
            f"[{source.citation}]" in final_text
            for source in sources
        ):
            final_text += "\n\nSources: " + ", ".join(
                f"[{source.citation}]"
                for source in sources
            )

        route_names = {call.get("name") for call in calls}

        if {
            "search_knowledge_base",
            "search_web",
        }.issubset(route_names):
            route = "kb+web"
        elif "search_web" in route_names:
            route = "web"
        else:
            route = "kb"

        return AgentResult(
            answer=final_text,
            sources=[asdict(source) for source in sources],
            route=route,
            tool_calls=calls,
            mode="real",
            warnings=list(self.warnings),
        )

    def ask(self, question: str) -> dict[str, Any]:
        """Public, error-safe API used by Streamlit and tests."""

        question = question.strip()

        if not question:
            return AgentResult(
                answer="Please enter a non-empty question.",
                sources=[],
                route="none",
                tool_calls=[],
                mode=self.mode,
                warnings=list(self.warnings),
            ).to_dict()

        try:
            result = (
                self._real_answer(question)
                if self.mode == "real"
                else self._stub_answer(question)
            )
        except Exception as error:
            # A real provider failure should not make the UI unusable.
            fallback = self._stub_answer(question)
            fallback.warnings.append(
                "Real execution failed and the deterministic fallback was "
                f"used: {type(error).__name__}: {error}"
            )
            result = fallback

        return result.to_dict()

    def status(self) -> dict[str, Any]:
        """Return non-secret diagnostics for the Streamlit sidebar."""

        return {
            "mode": self.mode,
            "groq_model": self.settings.groq_model,
            "embedding_backend": self.settings.embedding_backend,
            "groq_key_present": bool(
                os.getenv("GROQ_API_KEY", "").strip()
            ),
            "tavily_key_present": bool(
                os.getenv("TAVILY_API_KEY", "").strip()
            ),
            "google_key_present": bool(
                os.getenv("GOOGLE_API_KEY", "").strip()
            ),
            "langsmith": self.tracing,
            "knowledge_base_documents": len(KNOWLEDGE_BASE),
        }


@lru_cache(maxsize=1)
def get_service() -> AgenticRAGService:
    """Return one cached service instance per Python process."""

    return AgenticRAGService()
