"""Streamlit interface for the Agentic RAG service."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import streamlit as st
from dotenv import load_dotenv

from rag_agent import get_service

load_dotenv()

st.set_page_config(
    page_title="Agentic RAG Assistant",
    page_icon="🔎",
    layout="wide",
)


@st.cache_resource(show_spinner="Building the vector index…")
def load_service():
    """Initialize the vector index and agent only once."""

    return get_service()


def inspect_notebook(path: Path) -> dict[str, Any]:
    """Load agentic_rag.ipynb as text and report safe metadata.

    The exercise scaffold explicitly asks app.py to attempt a text load.
    The application never executes notebook code.
    """

    try:
        raw_text = path.read_text(encoding="utf-8")
        notebook = json.loads(raw_text)

        return {
            "loaded": True,
            "bytes": len(raw_text.encode("utf-8")),
            "cells": len(notebook.get("cells", [])),
            "error": None,
        }
    except Exception as error:
        return {
            "loaded": False,
            "bytes": 0,
            "cells": 0,
            "error": f"{type(error).__name__}: {error}",
        }


def render_sources(sources: list[dict[str, Any]]) -> None:
    """Render source records without trusting them as HTML."""

    if not sources:
        st.info("No source records were returned.")
        return

    for source in sources:
        citation = source.get("citation", "unknown")
        title = source.get("title", citation)
        url = source.get("url")
        snippet = source.get("snippet", "")
        origin = source.get("origin", "unknown")

        if url:
            st.markdown(f"- **[{citation}] [{title}]({url})** · `{origin}`")
        else:
            st.markdown(f"- **[{citation}] {title}** · `{origin}`")

        if snippet:
            st.caption(snippet[:400])


st.title("🔎 Agentic RAG Assistant")
st.write(
    "The assistant searches a local FAISS index first and can use Tavily "
    "for current or external information."
)

notebook_status = inspect_notebook(
    Path(__file__).with_name("agentic_rag.ipynb")
)

try:
    service = load_service()
    service_status = service.status()
except Exception as error:
    service = None
    service_status = {
        "mode": "unavailable",
        "initialization_error": f"{type(error).__name__}: {error}",
    }

with st.sidebar:
    st.header("Runtime status")
    st.json(service_status)

    st.header("Notebook")
    if notebook_status["loaded"]:
        st.success(
            "agentic_rag.ipynb loaded as text: "
            f"{notebook_status['cells']} cells, "
            f"{notebook_status['bytes']} bytes."
        )
    else:
        st.warning(
            "The notebook could not be loaded: "
            f"{notebook_status['error']}"
        )

    st.caption(
        "Secret values are never displayed. Only presence/absence is shown."
    )

with st.form("question_form"):
    question = st.text_area(
        "Question",
        value="How should an Agentic RAG system handle weak evidence?",
        height=120,
        max_chars=2000,
        help=(
            "Ask about the internal RAG notes or a current topic that "
            "may require web search."
        ),
    )

    submitted = st.form_submit_button(
        "Submit",
        type="primary",
        use_container_width=True,
    )

if submitted:
    if not question.strip():
        st.warning("Please enter a question.")
        st.stop()

    if service is None:
        st.error(
            "The Agentic RAG service could not initialize. "
            "Review the sidebar diagnostics."
        )
        st.stop()

    with st.spinner("Planning, retrieving, and synthesizing…"):
        result = service.ask(question)

    st.subheader("Answer")
    st.markdown(result["answer"])

    metric_columns = st.columns(3)
    metric_columns[0].metric("Mode", result["mode"])
    metric_columns[1].metric("Route", result["route"])
    metric_columns[2].metric("Sources", len(result["sources"]))

    if result["warnings"]:
        with st.expander("Warnings", expanded=True):
            for warning in result["warnings"]:
                st.warning(warning)

    with st.expander("Sources", expanded=True):
        render_sources(result["sources"])

    with st.expander("Tool calls"):
        st.json(result["tool_calls"])
