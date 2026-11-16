# this_file: src/fontlab_remopy/mcp/compat.py
# SPDX-License-Identifier: Apache-2.0
"""The few MCP SDK differences between v1 (camelCase, RootModel) and v2 (snake_case)."""
from __future__ import annotations

from typing import Any


def field(model: Any, snake: str, camel: str) -> Any:
    """Read a protocol field: v2 models use snake_case, v1 models camelCase."""
    return getattr(model, snake) if hasattr(model, snake) else getattr(model, camel)


def is_error(result: Any) -> bool:
    return bool(field(result, "is_error", "isError"))


def next_cursor(page: Any) -> str | None:
    return field(page, "next_cursor", "nextCursor")


def wire(model: Any) -> dict[str, Any]:
    """Wire-format (camelCase) dump on both SDK lines."""
    return model.model_dump(by_alias=True, mode="json")


def unwrap(message: Any) -> Any:
    """The JSON-RPC message inside a SessionMessage (v1 wraps it in a RootModel)."""
    inner = message.message
    return getattr(inner, "root", inner)


def tool_schema(tool: Any) -> Any:
    """A Tool's input schema (v2 ``input_schema``, v1 ``inputSchema``)."""
    return getattr(tool, "input_schema", None) or getattr(tool, "inputSchema", None)


def unknown_arguments(schema: Any, arguments: dict[str, Any]) -> list[str]:
    """Argument names a strict schema does not declare; [] when anything goes.

    FontLab silently drops unknown names, so an absent ``additionalProperties``
    counts as strict. Only absent or ``false`` is strict; ``true`` or a schema
    such as ``{}`` admits any name.
    """
    if not isinstance(schema, dict):
        return []
    if schema.get("additionalProperties", False) is not False:
        return []
    allowed = schema.get("properties")
    if not isinstance(allowed, dict):
        return []
    return sorted(set(arguments) - set(allowed))


def refuse_unknown(name: str, schema: Any, arguments: dict[str, Any]) -> None:
    """Raise ``ValueError`` naming the unknown and the allowed arguments."""
    unknown = unknown_arguments(schema, arguments)
    if unknown:
        raise ValueError(
            f"Unknown argument(s) for FontLab tool {name!r}: {', '.join(unknown)}. "
            f"Allowed: {', '.join(sorted(schema['properties']))}"
        )
