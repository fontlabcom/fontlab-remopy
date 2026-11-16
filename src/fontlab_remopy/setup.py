# this_file: src/fontlab_remopy/setup.py
# SPDX-License-Identifier: Apache-2.0
"""Bootstrap native MCP through a nonce-verified FontLab macro."""
from __future__ import annotations

import asyncio
import json
import shutil
import tempfile
import time
import uuid
from dataclasses import dataclass
from pathlib import Path

from mcp.types import Tool

from .mcp import probe_tools
from .platforms import DEFAULT_APP, submit_script


@dataclass(frozen=True)
class SetupResult:
    tools: list[Tool]
    execution_verified: bool = True


def _script(marker: Path, nonce: str) -> str:
    return f"""import json, fontlab
from pathlib import Path
try:
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


async def setup_mcp(app: str | Path = DEFAULT_APP, command: str | None = None,
                    timeout: float = 15) -> SetupResult:
    """Enable MCP once, prove macro completion, then authenticate/catalogue.

    On failure, the unique local macro/status files remain for inspection.
    Timeout does not establish whether the preference change executed.
    """
    if timeout <= 0:
        raise ValueError('Setup timeout must be positive')
    folder = Path(tempfile.mkdtemp(prefix='fontlab-remopy-setup-'))
    marker, script = folder/'result.json', folder/'enable.vfpy'
    nonce = uuid.uuid4().hex
    script.write_text(_script(marker,nonce))
    deadline = time.monotonic() + timeout
    try:
        async with asyncio.timeout(timeout):
            await asyncio.to_thread(submit_script,script,app,timeout)
            await _confirmation(marker,nonce)
            tools = await probe_tools(command,timeout=max(0.001,deadline-time.monotonic()))
    except BaseException as error:
        error.add_note(f'Setup outcome may be unknown; inspect {folder}')
        raise
    shutil.rmtree(folder)
    return SetupResult(tools)
