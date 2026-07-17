# Agentic RAG Streamlit App

A small Agentic RAG project using:

- Streamlit for the interface;
- FAISS for the local vector index;
- LangChain `create_agent`, powered by LangGraph;
- Groq for real tool-calling generation;
- Tavily for live web search;
- optional LangSmith tracing;
- deterministic stub mode for key-free testing.

## Architecture

```text
Streamlit form
     ↓
AgenticRAGService.ask()
     ↓
search_knowledge_base tool ──→ FAISS
     ↓ when needed
search_web tool ─────────────→ Tavily
     ↓
Groq agent synthesis
     ↓
answer + citations + tool trace
```

## Why `rag_agent.py` exists

A notebook is useful for teaching and experiments, but importing or executing
notebook cells from Streamlit is fragile. The notebook therefore writes the
complete reusable implementation to `rag_agent.py`; both the notebook and
`app.py` import the same public API.

`app.py` still loads `agentic_rag.ipynb` as plain text, as requested by the
exercise scaffold, and reports the notebook cell count in the sidebar.

## Install

```bash
python -m venv .venv
source .venv/bin/activate
# Windows: .venv\Scripts\Activate.ps1

pip install -r requirements.txt
cp .env.example .env
```

Add at least:

```env
GROQ_API_KEY=...
TAVILY_API_KEY=...
```

## Run

```bash
streamlit run app.py
```

## Modes

### Auto mode

```env
AGENTIC_RAG_MODE=auto
```

Real mode is selected only when both required keys are present. Otherwise the
deterministic stub is used.

### Force real mode

```env
AGENTIC_RAG_MODE=real
```

Initialization fails clearly when a required key is missing.

### Force stub mode

```env
AGENTIC_RAG_MODE=stub
```

No external API is called.

## Embeddings

The default `hash` backend is deterministic and download-free:

```env
EMBEDDING_BACKEND=hash
```

To use a local sentence-transformer:

```env
EMBEDDING_BACKEND=huggingface
HF_EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

## LangSmith

Set a LangSmith key and enable tracing:

```env
LANGSMITH_API_KEY=...
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=agentic-rag-streamlit
```

The implementation also supports the course's legacy `LANGCHAIN_*` variable
names.

## Current APIs used

- `langchain.agents.create_agent` is used instead of the deprecated
  `langgraph.prebuilt.create_react_agent`.
- `langchain-tavily` is used instead of the deprecated community Tavily search
  tool.
- The default Groq model is `openai/gpt-oss-20b`.

## Test

```bash
pytest -q
```

Tests force stub mode and do not require API keys.

## Error handling

- Empty questions return a validation response.
- Tavily and agent calls have configurable timeouts.
- Real-provider failures fall back to deterministic mode.
- Tool results are parsed into auditable source records.
- The UI never shows secret values.
