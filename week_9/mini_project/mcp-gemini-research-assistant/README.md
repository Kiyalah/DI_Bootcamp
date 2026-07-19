# Gemini Multi-Server MCP Research Assistant

This project is a Google Colab-friendly agentic application that composes
three MCP servers:

1. `@modelcontextprotocol/server-filesystem`
2. `mcp-server-git`
3. a custom FastMCP server named `research_ops`

Gemini receives the complete MCP tool list and chooses the next tool call.
The Python code does not hard-code a fixed read → format → write → commit
chain.

## Theme

**Research Workspace Assistant**

The agent inspects research notes and source records, checks Git history,
extracts citation identifiers, produces a Markdown brief, saves it through
the Filesystem server, and versions the change through the Git server.

## Primary deliverable

Open `mcp_gemini_research_assistant.ipynb` in Google Colab and execute the
cells in order.

## Required secret

Add `GOOGLE_API_KEY` to Colab Secrets, or enter it securely when the
notebook asks. The key is never written into project files.

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
# Windows: .venv\Scripts\Activate.ps1

pip install -r requirements.txt
cp .env.example .env
```

Node.js and `npx` are also required for the Filesystem MCP server.

## Architecture

```text
User objective
     ↓
Gemini + LangChain agent
     ├── Filesystem MCP
     ├── Git MCP
     └── research_ops MCP
             ↓
     tool results return to Gemini
             ↓
     Gemini chooses the next tool or final response
```

## Security notes

- The Filesystem server is restricted to the demo workspace.
- The Git server is restricted to the demo repository.
- The notebook does not expose the whole Colab filesystem.
- Reference MCP servers are educational implementations; review security
  requirements before adapting the project to production.
- Do not put API keys inside files accessible to MCP tools.

## Live execution

A live end-to-end run requires:

- internet access;
- a valid Gemini API key;
- Node/npm;
- the ability to download the third-party MCP packages.

Static validation can be performed without the Gemini key.
