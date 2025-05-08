from typing import List, Any


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
