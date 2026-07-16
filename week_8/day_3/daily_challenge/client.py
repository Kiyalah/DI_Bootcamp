"""Minimal MCP client that connects to server.py over STDIO.

The client:
1. starts the server through the MCP CLI;
2. initializes an MCP session;
3. discovers resources, resource templates, and tools;
4. reads greeting://hello;
5. calls add(a=1, b=7).
"""

import asyncio
import os
import shutil
from pathlib import Path
from typing import Any

from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
from pydantic import AnyUrl


# Resolve server.py relative to this client file.
# This makes the client work even when launched from another directory.
SERVER_PATH = Path(__file__).resolve().with_name("server.py")


def find_mcp_command() -> str:
    """Return the MCP CLI path or raise a useful setup error."""
    command = shutil.which("mcp")

    if command is None:
        raise RuntimeError(
            "The 'mcp' command was not found. Activate the virtual "
            "environment and install 'mcp[cli]>=1.27,<2'."
        )

    return command


# StdioServerParameters describes the child process that the client starts.
#
# Equivalent terminal command:
#     mcp run /absolute/path/to/server.py
#
# os.environ.copy() forwards the current environment to the child process.
server_params = StdioServerParameters(
    command=find_mcp_command(),
    args=["run", str(SERVER_PATH)],
    env=os.environ.copy(),
)


def resource_template_uri(template: Any) -> str:
    """Read a resource-template URI across compatible SDK field names."""
    value = getattr(template, "uriTemplate", None)

    if value is None:
        value = getattr(template, "uri_template", None)

    return str(value)


def extract_resource_text(result: Any) -> str:
    """Extract the first text block from a ReadResourceResult."""
    for block in getattr(result, "contents", []):
        text = getattr(block, "text", None)

        if text is not None:
            return str(text)

    return str(result)


def extract_tool_value(result: Any) -> Any:
    """Extract a structured or text value from a CallToolResult.

    FastMCP commonly returns:
    - structuredContent = {"result": 8}
    - content = [TextContent(text="8")]

    Prefer structured data, then fall back to text.
    """
    structured = getattr(result, "structuredContent", None)

    if structured is None:
        structured = getattr(result, "structured_content", None)

    if isinstance(structured, dict):
        if "result" in structured:
            return structured["result"]

        return structured

    for block in getattr(result, "content", []):
        if isinstance(block, types.TextContent):
            return block.text

        text = getattr(block, "text", None)
        if text is not None:
            return text

    return str(result)


async def run() -> None:
    """Connect to the server, discover capabilities, and invoke them."""

    # stdio_client starts the server child process and exposes two streams:
    # - read_stream: messages coming from the server;
    # - write_stream: messages sent to the server.
    async with stdio_client(server_params) as (
        read_stream,
        write_stream,
    ):
        # ClientSession implements the MCP lifecycle and request methods.
        async with ClientSession(
            read_stream,
            write_stream,
        ) as session:
            # The client and server exchange protocol versions and
            # capabilities before any normal request is made.
            initialization = await session.initialize()

            print(
                "Connected server:",
                initialization.serverInfo.name,
            )

            # list_resources() returns concrete/static resources.
            resources_result = await session.list_resources()
            resource_uris = [
                str(resource.uri)
                for resource in resources_result.resources
            ]

            # greeting://{name} is dynamic, so it appears as a template.
            templates_result = (
                await session.list_resource_templates()
            )
            template_uris = [
                resource_template_uri(template)
                for template
                in templates_result.resourceTemplates
            ]

            # list_tools() returns tools and their JSON schemas.
            tools_result = await session.list_tools()
            tool_names = [
                tool.name
                for tool in tools_result.tools
            ]

            print("Static resources:", resource_uris)
            print("Resource templates:", template_uris)
            print("Tools:", tool_names)

            # Instantiate the template with name="hello".
            greeting_result = await session.read_resource(
                AnyUrl("greeting://hello")
            )
            greeting_text = extract_resource_text(
                greeting_result
            )

            print(
                "greeting://hello ->",
                greeting_text,
            )

            # Tool arguments are sent as a JSON-compatible dictionary.
            addition_result = await session.call_tool(
                "add",
                arguments={
                    "a": 1,
                    "b": 7,
                },
            )
            addition_value = extract_tool_value(
                addition_result
            )

            print("add(1, 7) ->", addition_value)

            # Simple assertions turn this demo into a smoke test.
            assert "greeting://{name}" in template_uris
            assert "add" in tool_names
            assert greeting_text == "Hello, hello!"
            assert str(addition_value) == "8"


def main() -> None:
    """Synchronous entry point for the asynchronous client."""
    asyncio.run(run())


if __name__ == "__main__":
    main()
