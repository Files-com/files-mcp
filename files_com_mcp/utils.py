import json
from typing import Any, List, Optional

# Cap each markdown table cell at this many characters. Log entities include
# fields like `request_json`, `response_json`, `body`, `changes`, and `message`
# that can hold kilobytes of free-form text and would otherwise destroy the
# table layout and blow up the LLM's token budget.
MAX_CELL_LEN = 200


def _format_cell(value: Any) -> str:
    """Render a single attribute value as a safe markdown table cell."""
    text = str(value) if value is not None else ""
    # Escape pipe (column separator) and collapse newlines so each row stays on one line.
    text = (
        text.replace("\\", "\\\\")
        .replace("|", "\\|")
        .replace("\r", " ")
        .replace("\n", " ")
    )
    if len(text) > MAX_CELL_LEN:
        text = text[: MAX_CELL_LEN - 1] + "…"
    return text


def object_list_to_markdown_table(
    items: List[Any],
    default_attributes: List[str],
    fields: Optional[List[str]] = None,
) -> str:
    """
    Convert a list of objects into a Markdown table.

    :param items: List of objects (same type) to convert.
    :param default_attributes: Attribute names used when `fields` is not provided.
    :param fields: Optional caller-supplied subset of attribute names. When set
        and non-empty, overrides `default_attributes`. Attributes the item does
        not define render as empty cells.
    :return: A string containing the Markdown-formatted table.
    """
    if not items:
        return "*(no data)*"

    attributes = fields if fields else default_attributes
    if not attributes:
        return "*(no columns selected)*"

    # Header row
    table_lines = ["| " + " | ".join(attributes) + " |"]

    # Separator row
    table_lines.append("| " + " | ".join("---" for _ in attributes) + " |")

    # Data rows
    for obj in items:
        values = [_format_cell(getattr(obj, attr, "")) for attr in attributes]
        table_lines.append("| " + " | ".join(values) + " |")

    return "\n".join(table_lines)


def coerce_json(value: Any) -> Any:
    # Some MCP clients (notably Claude Cowork) serialize object/array tool
    # parameters as JSON strings instead of native JSON values, which breaks
    # Pydantic validation of `dict`/`list` fields. Parse a JSON string back
    # into its native shape; leave anything else untouched.
    if isinstance(value, str):
        try:
            return json.loads(value)
        except (json.JSONDecodeError, ValueError):
            return value
    return value


def context_api_key(context: Any) -> str:
    """Safely extract the Files.com API key from an MCP request context."""
    request_context = getattr(context, "request_context", None)
    if request_context is None:
        return ""

    session = getattr(request_context, "session", None)
    if session is None:
        return ""

    return str(getattr(session, "_files_com_api_key", "") or "")
