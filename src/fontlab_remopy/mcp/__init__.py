# this_file: src/fontlab_remopy/mcp/__init__.py
# SPDX-License-Identifier: Apache-2.0
"""Authenticated native MCP calls through the MCP SDK (v1 or v2) and relay."""
from __future__ import annotations

import asyncio
import json
import os
import sys
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.types import CallToolResult, PaginatedRequestParams, Tool

from ..platforms import find_bridge
from .compat import is_error, next_cursor, refuse_unknown, tool_schema, wire


class NativeExecutionError(RuntimeError):
    """Native execution completed with a tool or embedded Python error."""
    def __init__(self, payload: dict[str, Any]) -> None:
        self.payload = payload
        super().__init__('FontLab execution failed: '+str(payload.get('error',payload)))


def bridge_parameters(command: str) -> StdioServerParameters:
    """Use one SDK relay for all callers, including external coding agents."""
    return StdioServerParameters(command=sys.executable,
        args=['-m','fontlab_remopy.mcp.relay',command],env=os.environ.copy())


@asynccontextmanager
async def _session(command: str | None, timeout: float) -> AsyncIterator[ClientSession]:
    if timeout <= 0:
        raise ValueError('MCP timeout must be positive')
    bridge = find_bridge(command)
    if bridge is None:
        raise FileNotFoundError('No executable FontLab MCP bridge found')
    async with (
        asyncio.timeout(timeout),
        stdio_client(bridge_parameters(bridge)) as (read,write),
        ClientSession(read,write) as session,
    ):
        await session.initialize()
        yield session


async def _list_all(session: ClientSession) -> list[Tool]:
    tools: list[Tool] = []
    cursor = None
    while True:
        page = await session.list_tools(params=PaginatedRequestParams(cursor=cursor))
        tools.extend(page.tools)
        cursor = next_cursor(page)
        if not cursor:
            return tools


async def probe_tools(command: str | None = None, timeout: float = 8) -> list[Tool]:
    """Discover every page; initialization alone does not prove host reachability."""
    async with _session(command,timeout) as session:
        return await _list_all(session)


async def call_tool(name: str, arguments: dict[str, Any] | None = None,
                    command: str | None = None, timeout: float = 30,
                    *, check_arguments: bool = True) -> CallToolResult:
    """Return the actual SDK result; never retry a mutation after timeout.

    Unknown argument names raise ``ValueError`` before anything is sent, because
    FontLab silently drops them. This costs one catalogue request per call.
    """
    if arguments is not None and not isinstance(arguments, dict):
        raise TypeError('MCP tool arguments must be a dictionary')
    async with _session(command,timeout) as session:
        if check_arguments and arguments:
            schemas = {t.name: tool_schema(t) for t in await _list_all(session)}
            refuse_unknown(name, schemas.get(name), arguments)
        result = await session.call_tool(name,arguments=arguments or {})
    return result


async def run_python(code: str, command: str | None = None, timeout: float = 30) -> dict[str, Any]:
    """Require both transport success and a native execution success payload."""
    result = await call_tool('run_python',{'code':code},command,timeout,check_arguments=False)
    if is_error(result):
        raise NativeExecutionError(wire(result))
    for item in result.content:
        if item.type != 'text':
            continue
        payload = json.loads(item.text)
        if not isinstance(payload,dict) or not isinstance(payload.get('success'),bool):
            raise RuntimeError('Unexpected FontLab run_python payload')  # noqa: TRY004 - preserve the public malformed-response exception
        if not payload['success']:
            raise NativeExecutionError(payload)
        return payload
    raise RuntimeError('FontLab run_python returned no execution payload')


async def execute_script(path: str | Path, command: str | None = None, timeout: float = 30) -> dict[str, Any]:
    """Execute .flpy/.vfpy text via native MCP and preserve script filename context."""
    path = Path(path).expanduser().resolve()
    source = path.read_text(encoding='utf-8-sig')
    namespace = {'__name__':'__main__','__file__':str(path)}
    code = f'exec(compile({source!r}, {str(path)!r}, "exec"), {namespace!r})'
    return await run_python(code,command,timeout)
