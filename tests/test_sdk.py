# this_file: tests/test_sdk.py
# SPDX-License-Identifier: Apache-2.0
"""Real SDK framing, cancellation, discovery and process cleanup."""
import asyncio
import os
import sys
from pathlib import Path
from unittest.mock import AsyncMock

import pytest
from mcp.types import CallToolResult, TextContent

from fontlab_remopy import call_tool, find_bridge, mcp, probe_tools
from fontlab_remopy.mcp.compat import is_error


def test_explicit_missing_bridge_does_not_fall_back(monkeypatch):
    monkeypatch.setenv('FONTLAB_MCP_COMMAND','/missing/bridge')
    assert find_bridge() is None


@pytest.fixture
def bridge(tmp_path,monkeypatch):
    path = tmp_path/'FontLab fixture bridge'
    path.write_text('#!'+sys.executable+'\n'+(Path(__file__).parent/'fixtures/mcp_server.py').read_text())
    path.chmod(0o755)
    monkeypatch.setenv('AIDUS_MCP_TEST_LOG',str(tmp_path/'calls.txt'))
    return path


@pytest.mark.asyncio
@pytest.mark.parametrize("relay_module", ["fontlab_remopy.mcp.relay", "fontlab_remopy.mcp_bridge"])
async def test_real_sdk_discovers_and_executes_fixture_once(bridge, monkeypatch, relay_module):
    parameters = mcp.bridge_parameters

    def bridge_parameters(command):
        result = parameters(command)
        result.args[1] = relay_module
        return result

    monkeypatch.setattr(mcp, 'bridge_parameters', bridge_parameters)
    tools = await probe_tools(str(bridge))
    assert {tool.name for tool in tools} == {'list_fonts','run_python'}
    result = await call_tool('list_fonts',command=str(bridge))
    assert is_error(result) is False
    assert 'Fixture' in result.content[0].text
    assert Path(os.environ['AIDUS_MCP_TEST_LOG']).read_text() == 'list_fonts called'


@pytest.mark.asyncio
async def test_hung_bridge_times_out_and_its_process_is_gone(tmp_path):
    path,pidpath = tmp_path/'hung bridge',tmp_path/'pid.txt'
    path.write_text('#!'+sys.executable+'\nimport os,time\nfrom pathlib import Path\nPath('+repr(str(pidpath))+').write_text(str(os.getpid()))\ntime.sleep(60)\n')
    path.chmod(0o755)
    with pytest.raises((TimeoutError,ExceptionGroup)):
        await asyncio.wait_for(probe_tools(str(path),timeout=0.25),timeout=5)
    assert pidpath.is_file(), 'test never launched its hung subprocess'
    pid = int(pidpath.read_text())
    with pytest.raises(ProcessLookupError):
        os.kill(pid,0)


@pytest.mark.asyncio
async def test_real_tool_error_stays_error(monkeypatch):
    result = CallToolResult(isError=True,content=[TextContent(type='text',text='denied')])
    mocked = AsyncMock(return_value=result)
    monkeypatch.setattr(mcp,'call_tool',mocked)
    with pytest.raises(mcp.NativeExecutionError):
        await mcp.run_python('print(42)')
    assert mocked.await_count == 1, 'tool failures must not trigger an automatic retry'


def test_cli_when_tools_and_call_then_wire_format_camel_case(bridge,capsys):
    from fontlab_remopy.cli import main
    assert main(['--bridge',str(bridge),'--timeout','20','tools']) == 0
    tools = capsys.readouterr().out
    assert '"inputSchema"' in tools and '"input_schema"' not in tools
    assert main(['--bridge',str(bridge),'--timeout','20','call','list_fonts']) == 0
    called = capsys.readouterr().out
    assert '"isError": false' in called and '"is_error"' not in called
