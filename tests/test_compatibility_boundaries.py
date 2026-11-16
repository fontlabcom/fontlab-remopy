# this_file: tests/test_compatibility_boundaries.py
# SPDX-License-Identifier: Apache-2.0
"""Compatibility contracts for the modules moved in 1.2, without a native host."""

import builtins
import importlib
import sys
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import pytest

from fontlab_remopy import client, host, platforms, remote
from fontlab_remopy.actions import Controls


@pytest.mark.parametrize(
    "method,tool",
    [
        ("font_info", "get_font_info"), ("glyph_info", "get_glyph"),
        ("list_glyphs", "list_glyphs"), ("font_metrics", "get_font_metrics"),
        ("glyph_metrics", "get_glyph_metrics"), ("run_actions", "run_actions"),
        ("output", "get_python_output"), ("open_font", "open_font"),
        ("new_font", "new_font"), ("save_font", "save_font"),
        ("close_font", "close_font"), ("activate_font", "set_active_font"),
        ("activate_glyph", "set_active_glyph"), ("set_font_metrics", "set_font_metrics"),
        ("set_glyph_metrics", "set_glyph_metrics"),
    ],
)
def test_named_action_when_called_then_preserves_tool_and_arguments(method, tool):
    controls = Controls()
    controls.tool = Mock(return_value=object())
    assert getattr(controls, method)(font_id=42) is controls.tool.return_value
    controls.tool.assert_called_once_with(tool, font_id=42)


@pytest.mark.parametrize("name", ["fontlab", "fontlab_dependency"])
def test_host_when_import_fails_then_only_missing_host_is_translated(monkeypatch, name):
    original_import = builtins.__import__
    missing = ModuleNotFoundError("missing host dependency", name=name)

    def importing(module, *args, **kwargs):
        if module == "fontlab":
            raise missing
        return original_import(module, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", importing)
    expected = RuntimeError if name == "fontlab" else ModuleNotFoundError
    with pytest.raises(expected) as caught:
        host.enable_mcp()
    assert (caught.value.__cause__ if name == "fontlab" else caught.value) is missing


def test_platform_dispatch_when_not_macos_then_both_operations_name_platform(monkeypatch):
    try:
        with monkeypatch.context() as patch:
            patch.setattr(sys, "platform", "linux")
            importlib.reload(platforms)
            for function, args in (
                (platforms.launch, ()), (platforms.submit_script, ("script.flpy",)),
            ):
                with pytest.raises(NotImplementedError, match="platform: linux"):
                    function(*args)
    finally:
        importlib.reload(platforms)


def test_client_when_bridge_missing_then_releases_portal_and_can_close(monkeypatch):
    monkeypatch.setattr(client, "find_bridge", lambda _: None)
    connection = client.FontLab()
    with pytest.raises(FileNotFoundError, match="bridge"):
        connection.__enter__()
    assert connection._portal is None and connection._stack is None
    connection.close()


@pytest.mark.parametrize("timeout", [0, -1, float("nan"), float("inf")])
def test_client_when_timeout_invalid_then_refuses_connection(timeout):
    with pytest.raises(ValueError, match="positive"):
        client.AsyncFontLab(timeout=timeout)


@pytest.mark.asyncio
async def test_client_when_already_connected_then_refuses_reentry_and_paginates():
    connection = client.AsyncFontLab()
    connection._session = SimpleNamespace(list_tools=AsyncMock(side_effect=[
        SimpleNamespace(tools=["first"], next_cursor="next"),
        SimpleNamespace(tools=["second"], next_cursor=None),
    ]))
    with pytest.raises(RuntimeError, match="already connected"):
        await connection.__aenter__()
    assert await connection.tools() == ["first", "second"]
    assert connection._session.list_tools.call_args.kwargs["params"].cursor == "next"


def test_remote_when_not_sync_function_then_refuses_before_transport():
    async def asynchronous():
        pass

    for function in (len, asynchronous):
        with pytest.raises(ValueError, match="synchronous"):
            remote.remote_function(None, function)


@pytest.mark.parametrize("source", [None, "answer = 42"])
def test_remote_when_source_unavailable_or_not_function_then_guides_caller(monkeypatch, source):
    def function():
        return 42

    getsource = Mock(return_value=source) if source else Mock(side_effect=OSError("no source"))
    monkeypatch.setattr(remote.inspect, "getsource", getsource)
    with pytest.raises(ValueError, match="source"):
        remote.remote_function(None, function)


@pytest.mark.asyncio
async def test_remote_when_async_client_and_variadic_function_then_preserves_values():
    def function(*values: int, **keywords: int) -> int:
        return sum(values) + sum(keywords.values())

    connection = SimpleNamespace(run=AsyncMock(return_value=SimpleNamespace(value=42)))
    invoke = remote.remote_function(connection, function)
    assert await invoke(40, extra=2) == 42
    code = connection.run.call_args.args[0]
    assert "*values, **keywords" in code, "Remote annotations must not need local names"
    assert list(connection.run.call_args.kwargs.values()) == [[40], {"extra": 2}]
