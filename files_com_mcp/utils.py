from typing import Any, List


def object_list_to_markdown_table(
    items: List[Any], attributes: List[str]
) -> str:
    """
    Convert a list of objects into a Markdown table using selected attributes.

    :param items: List of objects (same type) to convert.
    :param attributes: List of attribute names (strings) to include as columns.
    :return: A string containing the Markdown-formatted table.
    """
    if not items:
        return "*(no data)*"

    # Header row
    table_lines = ["| " + " | ".join(attributes) + " |"]

    # Separator row
    table_lines.append("| " + " | ".join("---" for _ in attributes) + " |")

    # Data rows
    for obj in items:
        values = [str(getattr(obj, attr, "")) for attr in attributes]
        table_lines.append("| " + " | ".join(values) + " |")

    return "\n".join(table_lines)


def context_api_key(context: Any) -> str:
    """Safely extract the Files.com API key from an MCP request context."""
    request_context = getattr(context, "request_context", None)
    if request_context is None:
        return ""

    session = getattr(request_context, "session", None)
    if session is None:
        return ""

    return str(getattr(session, "_files_com_api_key", "") or "")
