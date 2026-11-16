# this_file: examples/native_smoke.py
# SPDX-License-Identifier: Apache-2.0
"""Read-only MCP smoke from an external interpreter with Remopy installed."""
import asyncio

from fontlab_remopy import probe_tools, run_python


async def main() -> None:
    tools = await probe_tools()
    assert any(tool.name == 'list_fonts' for tool in tools)
    result = await run_python('import fontlab; print(type(fontlab.flWorkspace.instance()).__name__)')
    assert result['success']
    print('Native catalogue and execution passed')

asyncio.run(main())
