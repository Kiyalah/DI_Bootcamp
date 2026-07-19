"""Custom MCP server for the Gemini Research Workspace Assistant.

The server deliberately focuses on operations that do not belong to the
generic Filesystem or Git MCP servers:

- extracting citation-like identifiers from research notes;
- validating structured source records;
- formatting a source-grounded Markdown research brief;
- providing a health-check tool.

It communicates through STDIO, so stdout is reserved for MCP protocol
messages. Avoid normal print statements in server tools.
"""

from __future__ import annotations

import re
from typing import Any, Dict, List

from fastmcp import FastMCP

mcp = FastMCP(name="research_ops")


@mcp.tool
def ping() -> str:
    """Return a short health-check response."""
    return "pong"


@mcp.tool
def extract_citations(text: str) -> Dict[str, Any]:
    """Extract URLs, DOI values, arXiv identifiers, and source labels.

    Args:
        text: Research notes or draft text to inspect.

    Returns:
        Deduplicated citation-like identifiers and a total item count.
    """

    if not isinstance(text, str) or not text.strip():
        return {
            "urls": [],
            "dois": [],
            "arxiv_ids": [],
            "source_labels": [],
            "count": 0,
        }

    # Match ordinary HTTP(S) URLs while avoiding common closing punctuation.
    url_pattern = re.compile(
        r"https?://[^\s\]\[()<>{}\"']+[^\s\]\[()<>{}\"'.,;:!?]"
    )

    # DOI identifiers normally begin with 10.<registrant>/<suffix>.
    doi_pattern = re.compile(
        r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+\b",
        flags=re.IGNORECASE,
    )

    # Support modern arXiv IDs and older archive/category forms.
    arxiv_pattern = re.compile(
        r"\b(?:arXiv:)?("
        r"(?:\d{4}\.\d{4,5})"
        r"|(?:[a-z-]+(?:\.[A-Z]{2})?/\d{7})"
        r")(?:v\d+)?\b",
        flags=re.IGNORECASE,
    )

    # Source labels such as [S1], [source:paper-a], or [kb:rag].
    source_label_pattern = re.compile(
        r"\[((?:S\d+)|(?:source:[^\]]+)|(?:kb:[^\]]+))\]",
        flags=re.IGNORECASE,
    )

    urls = sorted(set(url_pattern.findall(text)))
    dois = sorted(
        {
            match.rstrip(".,;:")
            for match in doi_pattern.findall(text)
        }
    )
    arxiv_ids = sorted(
        {
            match
            for match in arxiv_pattern.findall(text)
        }
    )
    source_labels = sorted(
        {
            match
            for match in source_label_pattern.findall(text)
        }
    )

    return {
        "urls": urls,
        "dois": dois,
        "arxiv_ids": arxiv_ids,
        "source_labels": source_labels,
        "count": (
            len(urls)
            + len(dois)
            + len(arxiv_ids)
            + len(source_labels)
        ),
    }


@mcp.tool
def validate_source_records(
    sources: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Validate source records before they are used in a research brief.

    Each source must contain a non-empty title and an HTTP(S) URL. Optional
    fields such as author, year, or note are preserved by the caller.

    Args:
        sources: List of dictionaries representing research sources.

    Returns:
        Validation status, valid records, and per-record error messages.
    """

    valid_records: List[Dict[str, Any]] = []
    errors: List[Dict[str, Any]] = []

    for index, source in enumerate(sources, start=1):
        record_errors: List[str] = []

        if not isinstance(source, dict):
            errors.append({
                "index": index,
                "errors": ["The source must be a dictionary."],
            })
            continue

        title = str(source.get("title", "")).strip()
        url = str(source.get("url", "")).strip()

        if not title:
            record_errors.append("title is required")

        if not re.match(r"^https?://", url, flags=re.IGNORECASE):
            record_errors.append(
                "url must start with http:// or https://"
            )

        if record_errors:
            errors.append({
                "index": index,
                "title": title or None,
                "errors": record_errors,
            })
        else:
            valid_records.append(source)

    return {
        "valid": not errors,
        "valid_count": len(valid_records),
        "error_count": len(errors),
        "valid_records": valid_records,
        "errors": errors,
    }


@mcp.tool
def format_research_brief(
    title: str,
    executive_summary: str,
    findings: List[str],
    sources: List[Dict[str, Any]],
) -> str:
    """Format a concise Markdown research brief with clickable sources.

    Args:
        title: Brief title.
        executive_summary: Short overview grounded in the supplied notes.
        findings: Important findings, ideally containing source labels.
        sources: Source dictionaries containing at least title and URL.

    Returns:
        A complete Markdown document.
    """

    cleaned_title = title.strip() or "Research Brief"
    cleaned_summary = executive_summary.strip()

    if not cleaned_summary:
        cleaned_summary = (
            "The available notes did not contain enough evidence for an "
            "executive summary."
        )

    cleaned_findings = [
        finding.strip()
        for finding in findings
        if isinstance(finding, str) and finding.strip()
    ]

    if not cleaned_findings:
        cleaned_findings = [
            "No sufficiently supported findings were supplied."
        ]

    lines = [
        f"# {cleaned_title}",
        "",
        "## Executive summary",
        "",
        cleaned_summary,
        "",
        "## Key findings",
        "",
    ]

    lines.extend(
        f"- {finding}"
        for finding in cleaned_findings
    )

    lines.extend([
        "",
        "## Sources",
        "",
    ])

    for index, source in enumerate(sources, start=1):
        source_title = str(
            source.get("title", f"Source {index}")
        ).strip()
        source_url = str(source.get("url", "")).strip()
        source_note = str(source.get("note", "")).strip()

        if source_url:
            line = (
                f"{index}. [{source_title}]({source_url})"
            )
        else:
            line = f"{index}. {source_title}"

        if source_note:
            line += f" — {source_note}"

        lines.append(line)

    if not sources:
        lines.append(
            "No validated source records were supplied."
        )

    lines.extend([
        "",
        "---",
        "",
        (
            "Generated by a Gemini agent orchestrating Filesystem, Git, "
            "and custom MCP servers."
        ),
        "",
    ])

    return "\n".join(lines)


if __name__ == "__main__":
    # STDIO is the default FastMCP transport and is explicit here because
    # the LangChain MCP client launches this file as a subprocess.
    mcp.run(transport="stdio")
