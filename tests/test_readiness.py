# this_file: tests/test_readiness.py
# SPDX-License-Identifier: Apache-2.0
"""Bounded startup, once-only setup and native Windows argument boundaries."""

import importlib
import sys
import time
from unittest.mock import AsyncMock, Mock

import pytest
from mcp.types import ErrorData

from fontlab_remopy import discovery, platforms, setup
from fontlab_remopy.mcp.compat import MCPError
from fontlab_remopy.platforms import windows


def offline(message='Cannot connect to FontLab 9. Start FontLab'):
    if MCPError.__name__ == 'MCPError':
        return MCPError(code=-32000, message=message)
    return MCPError(ErrorData(code=-32000, message=message))


@pytest.fixture
def ready_host(monkeypatch, tmp_path):
    monkeypatch.setattr(setup, 'find_bridge', Mock(return_value='selected bridge'))
    monkeypatch.setattr(setup, 'probe_tools', AsyncMock())
    monkeypatch.setattr(setup, 'setup_mcp', AsyncMock(return_value=setup.SetupResult(['tool'])))
    return tmp_path / 'FontLab 9.app'


@pytest.mark.asyncio
async def test_startup_when_called_from_running_loop_then_sync_api_sets_up_before_probe(ready_host):
    app = ready_host
    assert setup.ensure_ready(app, 'bridge', timeout=1).tools == ['tool']
    setup.setup_mcp.assert_awaited_once_with(app, 'selected bridge', timeout=1)
    setup.probe_tools.assert_not_awaited()
    setup.find_bridge.assert_called_once_with('bridge')


@pytest.mark.asyncio
@pytest.mark.parametrize('error', [PermissionError('refused'), offline('FontLab MCP authentication failed.'), ValueError('schema')])
async def test_startup_when_setup_fails_then_preserves_error_without_replay(ready_host, error):
    setup.setup_mcp.side_effect = error
    with pytest.raises(type(error)) as caught:
        await setup._ensure_ready(ready_host, 'bridge', 1)
    assert caught.value is error
    setup.setup_mcp.assert_awaited_once()
    setup.probe_tools.assert_not_awaited()


@pytest.mark.asyncio
async def test_startup_when_bridge_missing_then_refuses_before_submission(ready_host):
    setup.find_bridge.return_value = None
    with pytest.raises(FileNotFoundError, match='bridge'):
        await setup._ensure_ready(ready_host, None, 1)
    setup.setup_mcp.assert_not_awaited()
    setup.probe_tools.assert_not_awaited()


@pytest.mark.asyncio
async def test_startup_when_selected_bundle_has_bridge_then_uses_it(ready_host, monkeypatch):
    monkeypatch.setattr(setup.sys, 'platform', 'darwin')
    candidate = ready_host / 'Contents/MacOS/fontlab-mcp'
    candidate.parent.mkdir(parents=True)
    candidate.touch()
    await setup._ensure_ready(ready_host, None, 1)
    setup.find_bridge.assert_called_once_with(candidate)


@pytest.mark.asyncio
async def test_catalogue_when_full_deadline_available_then_does_not_cap_slow_valid_probe(monkeypatch):
    probe = AsyncMock(return_value=['tool'])
    monkeypatch.setattr(setup, 'probe_tools', probe)
    assert await setup._wait_tools('bridge', time.monotonic() + 30) == ['tool']
    assert 29 < probe.call_args.kwargs['timeout'] <= 30


@pytest.mark.parametrize('timeout', [0, -1, float('nan'), float('inf')])
def test_startup_when_invalid_deadline_then_refuses_before_submission(ready_host, timeout):
    with pytest.raises(ValueError, match='positive and finite'):
        setup.ensure_ready(timeout=timeout)
    setup.setup_mcp.assert_not_awaited()


@pytest.mark.asyncio
async def test_catalogue_when_starting_then_retries_read_only_probes(monkeypatch):
    probe = AsyncMock(side_effect=[offline(), offline('MCP authentication token is unavailable.'), ['tool']])
    monkeypatch.setattr(setup, 'probe_tools', probe)
    assert await setup._wait_tools('bridge', time.monotonic() + 1) == ['tool']
    assert probe.await_count == 3
    assert all(0 < call.kwargs['timeout'] <= 1 for call in probe.call_args_list)


@pytest.mark.asyncio
async def test_catalogue_when_deadline_expires_then_stops_without_setup(monkeypatch):
    probe = AsyncMock(side_effect=offline())
    monkeypatch.setattr(setup, 'probe_tools', probe)
    started = time.monotonic()
    with pytest.raises(TimeoutError, match='startup deadline'):
        await setup._wait_tools('bridge', started + 0.01)
    assert time.monotonic() - started < 0.5
    probe.assert_awaited_once()


@pytest.mark.asyncio
async def test_catalogue_when_unrelated_sdk_error_then_does_not_retry(monkeypatch):
    error = ExceptionGroup('SDK transport', [offline(), PermissionError('no access')])
    monkeypatch.setattr(setup, 'probe_tools', AsyncMock(side_effect=error))
    with pytest.raises(ExceptionGroup) as caught:
        await setup._wait_tools('bridge', time.monotonic() + 1)
    assert caught.value is error
    setup.probe_tools.assert_awaited_once()


@pytest.mark.asyncio
async def test_setup_when_macro_unconfirmed_then_retains_script_without_replay(monkeypatch, tmp_path):
    folder = tmp_path / 'setup'
    folder.mkdir()
    monkeypatch.setattr(setup.tempfile, 'mkdtemp', lambda **_: str(folder))
    submit = Mock()
    monkeypatch.setattr(setup, 'submit_script', submit)
    monkeypatch.setattr(setup, 'probe_tools', AsyncMock())
    with pytest.raises(TimeoutError) as caught:
        await setup.setup_mcp(timeout=0.01)
    submit.assert_called_once()
    setup.probe_tools.assert_not_awaited()
    assert (folder / 'enable.vfpy').is_file()
    assert str(folder) in caught.value.__notes__[0]


def test_windows_when_launch_and_submit_then_preserves_argument_boundaries(monkeypatch, tmp_path):
    app = tmp_path / 'FontLab 9.exe'
    app.touch()
    script = tmp_path / 'script with spaces.vfpy'
    script.touch()
    monkeypatch.setattr(windows.sys, 'platform', 'win32')
    popen = Mock()
    monkeypatch.setattr(windows.subprocess, 'Popen', popen)
    windows.launch(app)
    popen.assert_called_with([str(app)])
    result = windows.submit_script(script, app)
    popen.assert_called_with([str(app), str(script)])
    assert result.path == script and result.execution_verified is False
    with pytest.raises(FileNotFoundError):
        windows.submit_script(tmp_path / 'missing', app)
    with pytest.raises(FileNotFoundError):
        windows.launch(tmp_path / 'missing')
    with pytest.raises(ValueError, match='positive'):
        windows.launch(app, timeout=float('nan'))
    monkeypatch.setattr(windows.sys, 'platform', 'darwin')
    with pytest.raises(NotImplementedError, match='Windows'):
        windows.launch(app)


def test_platform_dispatch_when_windows_then_selects_native_provider(monkeypatch):
    try:
        with monkeypatch.context() as patch:
            patch.setattr(sys, 'platform', 'win32')
            importlib.reload(platforms)
            assert platforms.launch is windows.launch
            assert platforms.submit_script is windows.submit_script
    finally:
        importlib.reload(platforms)


def test_bridge_discovery_when_windows_then_uses_installed_executable_sibling(monkeypatch, tmp_path):
    monkeypatch.delenv('FONTLAB_MCP_COMMAND', raising=False)
    monkeypatch.delenv('AIDUS_FONTLAB_MCP_COMMAND', raising=False)
    monkeypatch.setattr(discovery.sys, 'platform', 'win32')
    monkeypatch.setattr(discovery, 'DEFAULT_APP', tmp_path / 'FontLab 9.exe')
    monkeypatch.setattr(discovery.shutil, 'which', lambda _: None)
    bridge = str(tmp_path / 'fontlab-mcp.exe')
    monkeypatch.setattr(discovery.os, 'access', lambda path, _: path == bridge)
    assert discovery.find_bridge() == bridge
