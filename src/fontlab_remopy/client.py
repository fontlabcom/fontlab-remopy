# this_file: src/fontlab_remopy/client.py
# SPDX-License-Identifier: Apache-2.0
"""Reusable synchronous and asynchronous FontLab MCP connections."""

from __future__ import annotations

import asyncio
import json
import math
from contextlib import ExitStack, asynccontextmanager
from functools import partial
from pathlib import Path
from typing import Any, Self

from anyio.from_thread import start_blocking_portal
from mcp import ClientSession
from mcp.client.stdio import stdio_client
from mcp.types import PaginatedRequestParams

from .actions import Controls
from .mcp import NativeExecutionError, bridge_parameters
from .mcp.compat import is_error, next_cursor, refuse_unknown, tool_schema, wire
from .platforms import find_bridge
from .results import ExecutionResult, decode_execution, encode_execution


@asynccontextmanager
async def _connection(command: str | None, timeout: float):
    bridge = find_bridge(command)
    if bridge is None:
        raise FileNotFoundError("No executable FontLab MCP bridge found")
    async with (
        stdio_client(bridge_parameters(bridge)) as (read, write),
        ClientSession(read, write) as session,
    ):
        async with asyncio.timeout(timeout):
            await session.initialize()
        yield session


class AsyncFontLab(Controls):
    """One authenticated session; use ``async with`` and await each operation.

    Enter/exit on the same task, as required by the SDK's structured transport.
    Idle lifetime is unlimited. Calls use the configured timeout without retry.
    """

    def __init__(self, command: str | None = None, timeout: float = 30) -> None:
        if not math.isfinite(timeout) or timeout <= 0:
            raise ValueError("MCP timeout must be positive")
        self.command, self.timeout = command, timeout
        self._session = None
        self._context = None
        self._lock = asyncio.Lock()
        self._uncertain = False
        self._schemas: dict[str, Any] | None = None  # tool name -> inputSchema

    async def __aenter__(self) -> Self:
        if self._session is not None:
            raise RuntimeError("FontLab is already connected")
        self._context = _connection(self.command, self.timeout)
        self._lock = asyncio.Lock()
        self._session = await self._context.__aenter__()
        self._uncertain = False
        self._schemas = None
        return self

    async def __aexit__(self, *exc: object) -> None:
        try:
            # User/native script errors belong to the public caller, not the
            # transport task groups. Close normally so SDK teardown does not
            # repackage those errors into nested ExceptionGroups.
            await self._context.__aexit__(None, None, None)
        finally:
            self._session = self._context = None

    async def _call(self, operation, *args, **kwargs):
        async with self._lock:
            if self._session is None or self._uncertain:
                raise RuntimeError(
                    "Connect FontLab with a fresh context before calling"
                )
            try:
                async with asyncio.timeout(self.timeout):
                    return await getattr(self._session, operation)(*args, **kwargs)
            except (TimeoutError, asyncio.CancelledError) as error:
                self._uncertain = True
                error.add_note(
                    "FontLab execution outcome may be unknown; never retry automatically"
                )
                raise

    async def tools(self) -> list[Any]:
        """Discover the complete native tool catalogue (every page)."""
        result, cursor = [], None
        while True:
            page = await self._call(
                "list_tools", params=PaginatedRequestParams(cursor=cursor)
            )
            result.extend(page.tools)
            cursor = next_cursor(page)
            if not cursor:
                return result

    async def _check_arguments(self, name: str, arguments: dict[str, Any]) -> None:
        """Refuse argument names the tool's schema does not declare.

        FontLab silently drops unknown names, so a misspelt ``master`` on a write
        tool acts on the current master. Names only; values are not validated.
        """
        if self._schemas is None:
            self._schemas = {t.name: tool_schema(t) for t in await self.tools()}
        refuse_unknown(name, self._schemas.get(name), arguments)

    async def tool(self, name: str, **arguments: Any) -> Any:
        """Return the catalogue's JSON payload; preserve native/tool failures.

        Argument names are checked against the live catalogue (fetched once per
        connection); an unknown name raises ``ValueError`` before anything is sent.
        """
        json.dumps(arguments, allow_nan=False)
        await self._check_arguments(name, arguments)
        return await self._tool(name, arguments)

    async def _tool(self, name: str, arguments: dict[str, Any]) -> Any:
        result = await self._call("call_tool", name, arguments=arguments)
        if is_error(result):
            raise NativeExecutionError(wire(result))
        texts = [item.text for item in result.content if item.type == "text"]
        if len(texts) != 1:
            raise RuntimeError("FontLab tool returned no single JSON payload")
        return json.loads(texts[0])

    async def run(self, code: str, /, **variables: Any) -> ExecutionResult:
        """Execute ordinary Python with JSON variables and captured output."""
        return await self._execute(code, variables, "<fontlab-remopy>")

    async def fonts(self) -> list[dict[str, Any]]:
        """Return open-font records without the catalogue's outer object."""
        return (await self.list_fonts())["fonts"]

    async def _execute(self, code, variables, filename):
        wrapped, nonce = encode_execution(code, variables, filename)
        payload = await self._tool("run_python", {"code": wrapped})
        return decode_execution(payload, nonce)

    async def eval(self, expression: str, /, **variables: Any) -> Any:
        """Evaluate an expression and return its JSON-native Python value."""
        return (await self.run("result = (" + expression + "\n)", **variables)).value

    async def execute_script(
        self, path: str | Path, /, **variables: Any
    ) -> ExecutionResult:
        """Run a .flpy/.vfpy file like ``run``; ``__file__`` is its resolved path."""
        path = Path(path).expanduser().resolve()
        return await self._execute(
            path.read_text(encoding="utf-8-sig"), variables, str(path)
        )


class FontLab(Controls):
    """Simple Python control, including notebooks with a running event loop.

    ``with FontLab() as fl: answer = fl.eval('value + 2', value=40)``
    Owns its portal thread and bridge until close/context exit.
    """

    def __init__(self, command: str | None = None, timeout: float = 30) -> None:
        self._async = AsyncFontLab(command, timeout)
        self._stack = None
        self._portal = None

    def __enter__(self) -> Self:
        if self._stack is not None:
            raise RuntimeError("FontLab is already connected")
        stack = ExitStack()
        try:
            self._portal = stack.enter_context(start_blocking_portal())
            stack.enter_context(self._portal.wrap_async_context_manager(self._async))
        except BaseException:
            stack.close()
            self._portal = None
            raise
        self._stack = stack
        return self

    def __exit__(self, *exc: object) -> bool | None:
        try:
            return self._stack.__exit__(*exc)
        finally:
            self._stack = self._portal = None

    def close(self) -> None:
        """Idempotently release the authenticated bridge and portal thread."""
        if self._stack is not None:
            self.__exit__(None, None, None)

    def _call(self, method, *args, **kwargs):
        if self._portal is None:
            raise RuntimeError("Connect FontLab using a with context before calling")
        return self._portal.call(partial(getattr(self._async, method), *args, **kwargs))

    def tools(self) -> list[Any]:
        """Discover the complete authenticated native tool catalogue."""
        return self._call("tools")

    def fonts(self) -> list[dict[str, Any]]:
        """Return open-font records without the catalogue's outer object."""
        return self._call("fonts")

    def tool(self, name: str, **arguments: Any) -> Any:
        """Call any native catalogue tool by name; return its JSON payload."""
        return self._call("tool", name, **arguments)

    def run(self, code: str, /, **variables: Any) -> ExecutionResult:
        """Execute ordinary Python with JSON variables and captured output."""
        return self._call("run", code, **variables)

    def eval(self, expression: str, /, **variables: Any) -> Any:
        """Evaluate an expression and return its JSON-native Python value."""
        return self._call("eval", expression, **variables)

    def execute_script(self, path: str | Path, /, **variables: Any) -> ExecutionResult:
        """Run a .flpy/.vfpy file like ``run``; ``__file__`` is its resolved path."""
        return self._call("execute_script", path, **variables)
