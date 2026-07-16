"""Minimal MCP server exposed over STDIO.

The server provides:
- one tool: add(a, b)
- one resource template: greeting://{name}

Important STDIO rule:
Do not use print() for normal logging in this server. Standard output is
reserved for MCP JSON-RPC messages. Log to stderr or a file instead.
"""

from mcp.server.fastmcp import FastMCP


# FastMCP converts Python type hints and docstrings into MCP schemas.
# The server name is visible to clients during session initialization.
mcp = FastMCP("Demo")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Return the sum of two integers.

    Args:
        a: First integer.
        b: Second integer.

    Returns:
        The integer sum a + b.
    """
    return a + b


@mcp.resource("greeting://{name}")
def greet(name: str) -> str:
    """Return a personalized greeting resource.

    The URI is a resource template. A client can replace {name} with a
    concrete value, for example greeting://hello.

    Args:
        name: Value captured from the resource URI.

    Returns:
        A short greeting.
    """
    return f"Hello, {name}!"


def main() -> None:
    """Start the MCP server using the STDIO transport.

    STDIO is ideal for local development because the client starts the
    server as a child process and communicates through stdin/stdout.
    No TCP port, web server, or authentication setup is required.
    """
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
