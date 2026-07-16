"""Two-server MCP mini-agent with stub or optional real planning.

The agent connects to:
- local_notes_server.py
- airbnb_stub_server.py, or the real OpenBnB npm MCP server

It discovers tool schemas dynamically, prefixes tool names to avoid name
collisions, asks a deterministic stub or GitHub Models to plan calls, then
routes every call back to the correct MCP session.
"""

import asyncio
import copy
import json
import os
import re
import shutil
from pathlib import Path
from typing import Any

import requests
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client


BASE_DIR = Path(__file__).resolve().parent
NOTES_SERVER = BASE_DIR / "local_notes_server.py"
AIRBNB_STUB_SERVER = BASE_DIR / "airbnb_stub_server.py"

USE_REAL_AIRBNB = os.getenv(
    "USE_REAL_AIRBNB",
    "false",
).lower() == "true"

USE_REAL_LLM = os.getenv(
    "USE_REAL_LLM",
    "false",
).lower() == "true"

IGNORE_ROBOTS_TXT = os.getenv(
    "IGNORE_ROBOTS_TXT",
    "false",
).lower() == "true"

GITHUB_MODELS_URL = (
    "https://models.github.ai/inference/chat/completions"
)
GITHUB_API_VERSION = "2026-03-10"
GITHUB_MODEL = os.getenv(
    "GITHUB_MODEL",
    "openai/gpt-4.1",
)


def find_command(name: str) -> str:
    """Return an executable path or raise a clear setup error."""
    command = shutil.which(name)

    if command is None:
        raise RuntimeError(
            f"Required command {name!r} was not found in PATH."
        )

    return command


def build_base_env() -> dict[str, str]:
    """Forward the environment and optionally add an MCP HTTP token."""
    environment = os.environ.copy()
    token = os.getenv("MCP_HTTP_TOKEN", "").strip()

    if token:
        environment["MCP_HTTP_TOKEN"] = token

    return environment


def notes_server_params() -> StdioServerParameters:
    """Describe how to start the local notes MCP server."""
    return StdioServerParameters(
        command=find_command("mcp"),
        args=["run", str(NOTES_SERVER)],
        env=build_base_env(),
    )


def airbnb_server_params() -> StdioServerParameters:
    """Select the offline stub or the real OpenBnB npm server."""
    if not USE_REAL_AIRBNB:
        return StdioServerParameters(
            command=find_command("mcp"),
            args=["run", str(AIRBNB_STUB_SERVER)],
            env=build_base_env(),
        )

    # The official package documentation recommends npx -y.
    arguments = [
        "-y",
        "@openbnb/mcp-server-airbnb",
    ]

    # Respect robots.txt by default. This opt-in flag is for explicit tests.
    if IGNORE_ROBOTS_TXT:
        arguments.append("--ignore-robots-txt")

    return StdioServerParameters(
        command=find_command("npx"),
        args=arguments,
        env=build_base_env(),
    )


def get_input_schema(tool: Any) -> dict[str, Any]:
    """Read a tool schema across MCP SDK field naming variations."""
    schema = getattr(tool, "inputSchema", None)

    if schema is None:
        schema = getattr(tool, "input_schema", None)

    return copy.deepcopy(schema or {
        "type": "object",
        "properties": {},
    })


def convert_tool(
    tool: Any,
    prefix: str,
) -> dict[str, Any]:
    """Convert an MCP tool into an LLM function specification.

    Prefixes such as notes__ and airbnb__ make the source server explicit
    and prevent collisions when both servers expose similarly named tools.
    """
    function_name = f"{prefix}__{tool.name}"

    return {
        "type": "function",
        "function": {
            "name": function_name,
            "description": (
                f"[{prefix} MCP server] "
                f"{tool.description or 'MCP tool'}"
            ),
            "parameters": get_input_schema(tool),
        },
    }


def available_function_names(
    functions: list[dict[str, Any]],
) -> set[str]:
    """Return the set of function names visible to the planner."""
    return {
        item["function"]["name"]
        for item in functions
    }


def extract_city(prompt: str) -> str:
    """Extract one supported demo city from natural-language text."""
    lower_prompt = prompt.lower()

    for city in ["Paris", "London", "Abidjan"]:
        if city.lower() in lower_prompt:
            return city

    # Generic fallback for phrases such as "stays in Rome".
    match = re.search(
        r"\b(?:in|near)\s+([A-Z][A-Za-zÀ-ÿ' -]{1,40})",
        prompt,
    )

    if match:
        candidate = match.group(1).strip(" .,!?")
        # Stop before common clauses.
        candidate = re.split(
            r"\s+(?:for|with|under|and|from|on)\s+",
            candidate,
            maxsplit=1,
            flags=re.IGNORECASE,
        )[0]
        return candidate.strip()

    return "Paris"


def extract_integer(
    pattern: str,
    prompt: str,
    default: int | None = None,
) -> int | None:
    """Return the first captured integer for a regex pattern."""
    match = re.search(pattern, prompt, flags=re.IGNORECASE)
    return int(match.group(1)) if match else default


def extract_note(prompt: str) -> str | None:
    """Extract a note request from the user prompt."""
    match = re.search(
        r"(?:save|add|write|remember)\s+(?:a\s+)?note"
        r"(?:\s+that|\s*:)?\s+(.+)$",
        prompt,
        flags=re.IGNORECASE,
    )

    if not match:
        return None

    return match.group(1).strip(" .")


def stub_plan(
    prompt: str,
    functions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Create deterministic calls for a listing search and optional note."""
    available = available_function_names(functions)
    calls: list[dict[str, Any]] = []
    lower_prompt = prompt.lower()

    # Plan an Airbnb search for prompts related to stays or listings.
    if any(
        word in lower_prompt
        for word in [
            "airbnb",
            "stay",
            "stays",
            "listing",
            "listings",
            "apartment",
            "accommodation",
        ]
    ):
        search_name = "airbnb__airbnb_search"

        if search_name not in available:
            raise ValueError(
                "The Airbnb server did not advertise airbnb_search."
            )

        arguments: dict[str, Any] = {
            "location": extract_city(prompt),
            "adults": extract_integer(
                r"(\d+)\s+adults?",
                prompt,
                default=1,
            ),
        }

        max_price = extract_integer(
            r"(?:under|below|max(?:imum)?(?:\s+price)?(?:\s+of)?)"
            r"\s*[$€£]?\s*(\d+)",
            prompt,
        )
        limit = extract_integer(
            r"(?:find|show|give|return)\s+(\d+)\s+",
            prompt,
            default=2,
        )

        if max_price is not None:
            arguments["maxPrice"] = max_price

        # `limit` is supported by the local stub, not necessarily the real
        # OpenBnB tool. Include it only in stub mode.
        if not USE_REAL_AIRBNB:
            arguments["limit"] = limit

        calls.append({
            "name": search_name,
            "args": arguments,
        })

    note_text = extract_note(prompt)

    if note_text:
        note_name = "notes__add_note"

        if note_name not in available:
            raise ValueError(
                "The notes server did not advertise add_note."
            )

        calls.append({
            "name": note_name,
            "args": {"text": note_text},
        })

    if "list note" in lower_prompt or "show note" in lower_prompt:
        list_name = "notes__list_notes"

        if list_name in available:
            calls.append({
                "name": list_name,
                "args": {},
            })

    if not calls:
        raise ValueError(
            "The stub planner could not identify an Airbnb or notes task."
        )

    return calls


def github_models_plan(
    prompt: str,
    functions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Use GitHub Models to propose prefixed function calls."""
    token = os.getenv("GITHUB_TOKEN", "").strip()

    if not token:
        raise RuntimeError(
            "Set GITHUB_TOKEN or keep USE_REAL_LLM=false."
        )

    response = requests.post(
        GITHUB_MODELS_URL,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": GITHUB_API_VERSION,
            "Content-Type": "application/json",
        },
        json={
            "model": GITHUB_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Plan all tool calls needed for the user request. "
                        "You may use tools from both MCP servers. "
                        "Return tool calls only."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            "tools": functions,
            "tool_choice": "auto",
            "temperature": 0,
            "max_tokens": 500,
        },
        timeout=60,
    )
    response.raise_for_status()

    message = response.json()["choices"][0]["message"]
    raw_calls = message.get("tool_calls") or []
    calls: list[dict[str, Any]] = []

    for raw_call in raw_calls:
        function = raw_call["function"]
        raw_arguments = function.get("arguments", {})
        arguments = (
            json.loads(raw_arguments)
            if isinstance(raw_arguments, str)
            else raw_arguments
        )

        calls.append({
            "name": function["name"],
            "args": arguments,
        })

    if not calls:
        raise RuntimeError("The real LLM returned no tool calls.")

    return calls


def plan_tool_calls(
    prompt: str,
    functions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Select the stub or real planner."""
    if USE_REAL_LLM:
        return github_models_plan(prompt, functions)

    return stub_plan(prompt, functions)


def extract_tool_value(result: Any) -> Any:
    """Extract structured or text data from an MCP tool result."""
    structured = getattr(result, "structuredContent", None)

    if structured is None:
        structured = getattr(result, "structured_content", None)

    if isinstance(structured, dict):
        if set(structured) == {"result"}:
            return structured["result"]
        return structured

    texts: list[str] = []

    for block in getattr(result, "content", []):
        if isinstance(block, types.TextContent):
            texts.append(block.text)
            continue

        text = getattr(block, "text", None)
        if text is not None:
            texts.append(str(text))

    if len(texts) == 1:
        single = texts[0]
        try:
            return json.loads(single)
        except json.JSONDecodeError:
            return single

    return texts


def validate_call(
    call: dict[str, Any],
    prefixed_tools: dict[str, tuple[str, str]],
) -> None:
    """Reject unknown names or malformed planner arguments."""
    if not isinstance(call, dict):
        raise TypeError("Every tool call must be a dictionary.")

    name = call.get("name")
    arguments = call.get("args")

    if name not in prefixed_tools:
        raise ValueError(f"Unknown prefixed tool: {name!r}")

    if not isinstance(arguments, dict):
        raise TypeError(
            f"Arguments for {name!r} must be a dictionary."
        )


def compact_listing_summary(value: Any) -> str:
    """Create a readable deterministic summary for the stub run."""
    if not isinstance(value, dict):
        return str(value)

    listings = value.get("listings")

    if not isinstance(listings, list):
        return json.dumps(value, ensure_ascii=False)

    if not listings:
        return f"No listings found for {value.get('location', 'the location')}."

    lines = [
        f"Listings for {value.get('location', 'requested location')}:"
    ]

    for item in listings:
        lines.append(
            "- "
            f"{item.get('name')} — "
            f"{item.get('price_per_night')} per night — "
            f"rating {item.get('rating')} — "
            f"{item.get('url')}"
        )

    return "\n".join(lines)


async def orchestrate(prompt: str) -> dict[str, Any]:
    """Connect both servers, plan calls, route them, and return results."""
    notes_params = notes_server_params()
    airbnb_params = airbnb_server_params()

    async with stdio_client(notes_params) as (notes_read, notes_write):
        async with ClientSession(
            notes_read,
            notes_write,
        ) as notes_session:
            await notes_session.initialize()
            notes_tools_result = await notes_session.list_tools()

            async with stdio_client(airbnb_params) as (
                airbnb_read,
                airbnb_write,
            ):
                async with ClientSession(
                    airbnb_read,
                    airbnb_write,
                ) as airbnb_session:
                    await airbnb_session.initialize()
                    airbnb_tools_result = await airbnb_session.list_tools()

                    functions = [
                        *[
                            convert_tool(tool, "notes")
                            for tool in notes_tools_result.tools
                        ],
                        *[
                            convert_tool(tool, "airbnb")
                            for tool in airbnb_tools_result.tools
                        ],
                    ]

                    # Map each prefixed function back to its source server
                    # and original MCP tool name.
                    prefixed_tools: dict[
                        str,
                        tuple[str, str],
                    ] = {}

                    for tool in notes_tools_result.tools:
                        prefixed_tools[
                            f"notes__{tool.name}"
                        ] = ("notes", tool.name)

                    for tool in airbnb_tools_result.tools:
                        prefixed_tools[
                            f"airbnb__{tool.name}"
                        ] = ("airbnb", tool.name)

                    calls = plan_tool_calls(prompt, functions)
                    results: list[dict[str, Any]] = []

                    print("Notes tools:", [
                        tool.name
                        for tool in notes_tools_result.tools
                    ])
                    print("Airbnb tools:", [
                        tool.name
                        for tool in airbnb_tools_result.tools
                    ])
                    print("LLM/stub function names:", [
                        item["function"]["name"]
                        for item in functions
                    ])
                    print(
                        "Planner:",
                        "GitHub Models"
                        if USE_REAL_LLM
                        else "deterministic stub",
                    )
                    print("Prompt:", prompt)
                    print("tool_calls:", calls)

                    for call in calls:
                        validate_call(call, prefixed_tools)

                        prefix, original_name = prefixed_tools[
                            call["name"]
                        ]

                        session = (
                            notes_session
                            if prefix == "notes"
                            else airbnb_session
                        )

                        raw_result = await session.call_tool(
                            original_name,
                            arguments=call["args"],
                        )
                        value = extract_tool_value(raw_result)

                        record = {
                            "name": call["name"],
                            "args": call["args"],
                            "value": value,
                        }
                        results.append(record)
                        print("tool_result:", record)

                    # Produce a small deterministic final response in stub
                    # mode. The raw calls/results remain available above.
                    answer_parts: list[str] = []

                    for record in results:
                        if record["name"].startswith("airbnb__"):
                            answer_parts.append(
                                compact_listing_summary(record["value"])
                            )
                        elif record["name"] == "notes__add_note":
                            answer_parts.append(
                                f"Note: {record['value']}"
                            )
                        elif record["name"] == "notes__list_notes":
                            answer_parts.append(
                                f"Saved notes:\n{record['value']}"
                            )

                    final_answer = "\n\n".join(answer_parts)
                    print("\nFINAL ANSWER")
                    print(final_answer)

                    return {
                        "prompt": prompt,
                        "functions": functions,
                        "tool_calls": calls,
                        "tool_results": results,
                        "answer": final_answer,
                    }


def main() -> None:
    """Run the default demo from a normal terminal."""
    prompt = os.getenv(
        "DEMO_PROMPT",
        (
            "Find 2 Airbnb stays in Paris for 2 adults under $250 "
            "per night and save a note that I prefer a balcony."
        ),
    )

    asyncio.run(orchestrate(prompt))


if __name__ == "__main__":
    main()
