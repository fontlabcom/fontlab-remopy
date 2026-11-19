# this_file: tests/test_setup_relay_boundaries.py
# SPDX-License-Identifier: Apache-2.0
"""Prove setup confirmation and relay cleanup with isolated transport doubles."""

import asyncio
import json
import runpy
import sys
from contextlib import asynccontextmanager
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import pytest

from fontlab_remopy import setup
from fontlab_remopy.mcp import relay


@pytest.mark.asyncio
@pytest.mark.parametrize("failure", [False, True])
async def test_setup_when_submitted_then_proves_nonce_or_retains_failure_files(
    tmp_path, monkeypatch, failure
):
    folder = tmp_path / "setup-é-字"
    folder.mkdir()
    monkeypatch.setattr(setup.tempfile, "mkdtemp", lambda **_: str(folder))
    write_text = Path.write_text

    def windows_write_text(path, data, encoding=None, **kwargs):
        return write_text(path, data, encoding=encoding or "cp1252", **kwargs)

    monkeypatch.setattr(Path, "write_text", windows_write_text)
    prefs, items = Mock(), Mock()
    monkeypatch.setitem(sys.modules, "fontlab", SimpleNamespace(
        flPreferences=lambda: prefs, flItems=items,
    ))

    def submit(path, app, timeout):
        if failure:
            raise RuntimeError("submission failed")
        runpy.run_path(str(path))

    async def catalogue(*args, **kwargs):
        assert (folder / "result.json").is_file(), "Submit and confirm the .vfpy before any MCP probe"
        assert prefs.generalHideWarningDialogs is True
        return []

    probe = AsyncMock(side_effect=catalogue)
    monkeypatch.setattr(setup, "submit_script", submit)
    monkeypatch.setattr(setup, "probe_tools", probe)
    if failure:
        with pytest.raises(RuntimeError, match="submission failed") as caught:
            await setup.setup_mcp(command="bridge")
        assert (folder / "enable.vfpy").is_file(), "Retain unknown-outcome evidence"
        assert str(folder) in caught.value.__notes__[0]
        probe.assert_not_called()
    else:
        result = await setup.setup_mcp(command="bridge")
        assert result.execution_verified and result.tools == []
        assert not folder.exists(), "Remove setup evidence only after confirmed success"
        prefs.load.assert_called_once_with({"mcp.enabled": True})
        assert prefs.generalHideWarningDialogs is True
        items.notifyPreferencesChanged.assert_called_once_with()
        assert probe.call_args.args == ("bridge",)
        assert 0 < probe.call_args.kwargs["timeout"] <= 15


@pytest.mark.asyncio
async def test_confirmation_when_marker_arrives_then_waits_and_verifies(tmp_path, monkeypatch):
    marker = tmp_path / "result.json"

    async def write_marker(_):
        marker.write_text(json.dumps({"nonce": "expected", "success": True}))

    monkeypatch.setattr(setup.asyncio, "sleep", write_marker)
    await setup._confirmation(marker, "expected")
    with pytest.raises(RuntimeError, match="macro failed"):
        await setup._confirmation(marker, "different nonce")
    marker.write_text(json.dumps({"nonce": "expected", "success": False}))
    with pytest.raises(RuntimeError, match="macro failed"):
        await setup._confirmation(marker, "expected")
    with pytest.raises(ValueError, match="positive"):
        await setup.setup_mcp(timeout=0)


@pytest.mark.asyncio
@pytest.mark.parametrize("broken", [False, True])
async def test_relay_when_finished_or_failed_then_closes_both_writers(monkeypatch, broken):
    sent = asyncio.Event()
    messages = []

    async def read(value):
        yield value
        await sent.wait()

    async def send(value):
        messages.append(value)
        if len(messages) == 2:
            sent.set()

    upstream = SimpleNamespace(send=AsyncMock(side_effect=send), aclose=AsyncMock())
    downstream = SimpleNamespace(send=AsyncMock(side_effect=send), aclose=AsyncMock())
    request, response = object(), object()

    @asynccontextmanager
    async def stdio_client(params):
        assert params.command == "fixture bridge" and params.args == []
        yield read(response), upstream

    @asynccontextmanager
    async def stdio_server():
        yield read(ValueError("bad frame") if broken else request), downstream

    normalize = Mock(return_value=response)
    monkeypatch.setattr(relay, "stdio_client", stdio_client)
    monkeypatch.setattr(relay, "stdio_server", stdio_server)
    monkeypatch.setattr(relay, "normalize_result", normalize)
    if broken:
        with pytest.raises(ExceptionGroup, match="TaskGroup"):
            await relay.relay("fixture bridge")
    else:
        async with asyncio.timeout(2):
            await relay.relay("fixture bridge")
        assert request in messages and response in messages
        normalize.assert_called_once_with(response)
    upstream.aclose.assert_awaited_once()
    downstream.aclose.assert_awaited_once()


def test_legacy_relay_entry_when_run_then_calls_canonical_main(monkeypatch):
    main = Mock()
    monkeypatch.setattr(relay, "main", main)
    monkeypatch.delitem(sys.modules, "fontlab_remopy.mcp_bridge", raising=False)
    with pytest.warns(DeprecationWarning, match="use fontlab_remopy.mcp.relay"):
        runpy.run_module("fontlab_remopy.mcp_bridge", run_name="__main__")
    main.assert_called_once_with()


def test_package_entry_when_run_as_module_then_exits_with_cli_status(monkeypatch):
    from fontlab_remopy import cli

    main = Mock(return_value=7)
    monkeypatch.setattr(cli, "main", main)
    monkeypatch.delitem(sys.modules, "fontlab_remopy.__main__", raising=False)
    with pytest.raises(SystemExit) as exit_info:
        runpy.run_module("fontlab_remopy", run_name="__main__")
    assert exit_info.value.code == 7
    main.assert_called_once_with()


def test_relay_main_when_called_then_sets_process_grace_and_runs_bridge(monkeypatch):
    import mcp.client.stdio as sdk_stdio

    monkeypatch.setattr(sdk_stdio, "PROCESS_TERMINATION_TIMEOUT", sdk_stdio.PROCESS_TERMINATION_TIMEOUT)
    monkeypatch.setattr(sys, "argv", ["relay", "fixture bridge"])
    run = Mock()
    monkeypatch.setattr(relay.anyio, "run", run)
    relay.main()
    run.assert_called_once_with(relay.relay, "fixture bridge")
    assert sdk_stdio.PROCESS_TERMINATION_TIMEOUT == 0.25
