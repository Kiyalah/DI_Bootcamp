"""Local MCP notes server used by the mini-agent.

The server keeps notes in memory for the lifetime of one MCP process.
It exposes two tools:
- add_note(text)
- list_notes()

No database or LLM is involved.
"""

from mcp.server.fastmcp import FastMCP


# FastMCP converts the Python signatures and docstrings into MCP schemas.
mcp = FastMCP("LocalNotes")

# The list is intentionally in memory for a small educational example.
notes: list[str] = []


@mcp.tool()
def add_note(text: str) -> str:
    """Save one text note in memory.

    Args:
        text: The note that should be remembered.

    Returns:
        A confirmation containing the note number and saved text.
    """
    cleaned_text = text.strip()

    if not cleaned_text:
        return "The note was empty and was not saved."

    notes.append(cleaned_text)
    return f"Saved note #{len(notes)}: {cleaned_text}"


@mcp.tool()
def list_notes() -> str:
    """Return all notes saved during the current server session."""
    if not notes:
        return "No notes yet."

    # Use real line breaks so the result is easy to read.
    return "\n".join(
        f"{index}. {note}"
        for index, note in enumerate(notes, start=1)
    )


def main() -> None:
    """Start the notes server over STDIO."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
