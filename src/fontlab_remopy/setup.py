# this_file: src/fontlab_remopy/setup.py
# SPDX-License-Identifier: Apache-2.0
"""Bootstrap native MCP through a nonce-verified FontLab macro."""
from __future__ import annotations

import asyncio
import json
import math
import shutil
import sys
import tempfile
import time
import uuid
from dataclasses import dataclass
from functools import partial
from pathlib import Path

from anyio.from_thread import start_blocking_portal
from mcp.types import Tool

from .mcp import probe_tools
from .mcp.compat import MCPError
from .platforms import DEFAULT_APP, find_bridge, launch, submit_script


@dataclass(frozen=True)
class SetupResult:
    tools: list[Tool]
    execution_verified: bool = True


def _script(marker: Path, nonce: str) -> str:
    return f"""import json, fontlab
from pathlib import Path
try:
    fontlab.flPreferences().generalHideWarningDialogs = True
    fontlab.flPreferences().load({{'mcp.enabled': True}})
    fontlab.flItems.notifyPreferencesChanged()
    result = {{'nonce': {nonce!r}, 'success': True}}
except Exception as error:
    result = {{'nonce': {nonce!r}, 'success': False, 'error': str(error)}}
marker = Path({str(marker)!r})
temporary = marker.with_suffix('.tmp')
temporary.write_text(json.dumps(result))
temporary.replace(marker)
"""


async def _confirmation(marker: Path, nonce: str) -> None:
    while not marker.is_file():
        await asyncio.sleep(0.05)
    result = json.loads(marker.read_text())
    if result.get('nonce') != nonce or result.get('success') is not True:
        raise RuntimeError('FontLab MCP setup macro failed: '+str(result))


def _unavailable(error: Exception) -> bool:
    if isinstance(error, ExceptionGroup):
        return all(_unavailable(child) for child in error.exceptions)
    return isinstance(error, TimeoutError) or (
        isinstance(error, MCPError) and str(error).startswith((
            'Cannot connect to FontLab 9.',
            'MCP authentication token is unavailable.',
        ))
    )


async def _wait_tools(command: str | None, deadline: float) -> list[Tool]:
    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError('FontLab MCP did not become ready before the startup deadline')
        try:
            return await probe_tools(command, timeout=remaining)
        except Exception as error:
            if not _unavailable(error):
                raise
            await asyncio.sleep(min(0.1, max(0, deadline - time.monotonic())))


async def _ensure_ready(app: str | Path, command: str | None, timeout: float) -> SetupResult:
    app = Path(app).expanduser().resolve()
    candidate = app/'Contents/MacOS/fontlab-mcp' if sys.platform == 'darwin' else app.parent/'fontlab-mcp.exe'
    bridge = find_bridge(command if command is not None else (candidate if candidate.is_file() else None))
    if bridge is None:
        raise FileNotFoundError('No executable FontLab MCP bridge found')
    deadline = time.monotonic() + timeout
    async with asyncio.timeout(timeout):
        await asyncio.to_thread(launch, app, timeout)
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError('FontLab launch exceeded the startup deadline')
        try:
            return SetupResult(await probe_tools(bridge, timeout=remaining))
        except Exception as error:
            if not _unavailable(error):
                raise
        remaining = deadline-time.monotonic()
        if remaining <= 0:
            raise TimeoutError('FontLab MCP did not become ready before the startup deadline')
        return await setup_mcp(app, bridge, timeout=remaining)


def ensure_ready(app: str | Path = DEFAULT_APP, command: str | None = None,
                 timeout: float = 30) -> SetupResult:
    """Launch and prove MCP readiness before executing any user operation.

    An unavailable host receives one nonce-confirmed setup macro, enabling MCP
    and suppressing warning dialogs. Only read-only catalogue probes are retried.
    The startup deadline includes launch, setup and authentication. Failed setup
    retains its files and must not be automatically replayed.
    """
    if not math.isfinite(timeout) or timeout <= 0:
        raise ValueError('Startup timeout must be positive and finite')
    with start_blocking_portal() as portal:
        return portal.call(partial(_ensure_ready, app, command, timeout))


async def setup_mcp(app: str | Path = DEFAULT_APP, command: str | None = None,
                    timeout: float = 15) -> SetupResult:
    """Enable MCP once, prove macro completion, then authenticate/catalogue.

    On failure, the unique local macro/status files remain for inspection.
    Timeout does not establish whether the preference change executed.
    """
    if not math.isfinite(timeout) or timeout <= 0:
        raise ValueError('Setup timeout must be positive and finite')
    folder = Path(tempfile.mkdtemp(prefix='fontlab-remopy-setup-'))
    marker, script = folder/'result.json', folder/'enable.vfpy'
    nonce = uuid.uuid4().hex
    script.write_text(_script(marker,nonce), encoding='utf-8')
    deadline = time.monotonic() + timeout
    try:
        async with asyncio.timeout(timeout):
            await asyncio.to_thread(submit_script,script,app,timeout)
            await _confirmation(marker,nonce)
            tools = await _wait_tools(command, deadline)
    except BaseException as error:
        error.add_note(f'Setup outcome may be unknown; inspect {folder}')
        raise
    shutil.rmtree(folder)
    return SetupResult(tools)
