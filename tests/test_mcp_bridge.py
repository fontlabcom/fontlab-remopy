# this_file: tests/test_mcp_bridge.py
# SPDX-License-Identifier: Apache-2.0
"""Keep compatibility normalization narrow and preserve all MCP error details."""

from mcp import types
from mcp.shared.message import SessionMessage

from fontlab_remopy.mcp.compat import is_error, unwrap
from fontlab_remopy.mcp.relay import normalize_result


def message(inner):
    """SessionMessage on either SDK line (v1 wraps JSON-RPC in a RootModel)."""
    wrap = types.JSONRPCMessage
    return SessionMessage(wrap(inner) if callable(wrap) else inner)


def test_normalize_when_optional_flag_null_preserves_payload_and_request_id():
    original = message(
        types.JSONRPCResponse(
            jsonrpc="2.0",
            id="abc",
            result={"isError": None, "content": [{"type": "text", "text": "ok"}]},
        )
    )
    result = unwrap(normalize_result(original))
    assert result.id == "abc"
    assert result.result == {"content": [{"type": "text", "text": "ok"}]}
    assert not is_error(types.CallToolResult.model_validate(result.result))


def test_normalize_when_tool_error_preserves_true():
    original = message(types.JSONRPCResponse(jsonrpc="2.0", id=7, result={"isError": True, "content": []}))
    assert unwrap(normalize_result(original)).result["isError"] is True


def test_normalize_when_rpc_error_does_not_change_error():
    original = message(
        types.JSONRPCError(
            jsonrpc="2.0",
            id=7,
            error=types.ErrorData(code=-32001, message="Authentication failed"),
        )
    )
    assert unwrap(normalize_result(original)).error.message == "Authentication failed"


def test_compat_when_v1_or_v2_style_objects_then_same_answers():
    from types import SimpleNamespace

    from fontlab_remopy.mcp.compat import next_cursor, wire

    assert is_error(SimpleNamespace(isError=True)) and not is_error(SimpleNamespace(is_error=False))
    assert next_cursor(SimpleNamespace(nextCursor="a")) == "a"
    assert next_cursor(SimpleNamespace(next_cursor=None)) is None
    dumped = wire(types.CallToolResult(isError=True, content=[]))
    assert dumped["isError"] is True and "is_error" not in dumped
