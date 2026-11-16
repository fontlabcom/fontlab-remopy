# this_file: src/fontlab_remopy/mcp/relay.py
# SPDX-License-Identifier: Apache-2.0
"""SDK stdio relay for FontLab builds returning a null optional error flag."""

from __future__ import annotations

import os
import sys
from typing import TYPE_CHECKING

import anyio
from mcp import StdioServerParameters, types
from mcp.client.stdio import stdio_client
from mcp.server.stdio import stdio_server

from .compat import unwrap

if TYPE_CHECKING:
    from anyio.abc import ObjectReceiveStream, ObjectSendStream
    from mcp.shared.message import SessionMessage


def normalize_result(message: SessionMessage) -> SessionMessage:
    """Treat isError:null as an omitted optional flag, preserving real errors."""
    response = unwrap(message)
    if (
        isinstance(response, types.JSONRPCResponse)
        and response.result.get("isError", False) is None
    ):
        response.result.pop("isError")
    return message


async def relay(command: str) -> None:
    """Let the SDK own framing, subprocess lifetime and MCP message validation."""
    params = StdioServerParameters(command=command, args=[], env=os.environ.copy())
    async with (
        stdio_client(params) as (up_read, up_write),
        stdio_server() as (down_read, down_write),
    ):
        try:
            async with anyio.create_task_group() as group:

                async def forward(
                    source: ObjectReceiveStream[SessionMessage | Exception],
                    destination: ObjectSendStream[SessionMessage],
                    normalize: bool,
                ) -> None:
                    try:
                        async for message in source:
                            if isinstance(message, Exception):
                                raise message
                            await destination.send(normalize_result(message) if normalize else message)
                    finally:
                        group.cancel_scope.cancel()

                group.start_soon(forward, down_read, up_write, False)
                group.start_soon(forward, up_read, down_write, True)
        finally:
            # The SDK server transport waits for its writer to reach channel
            # EOF. Close it before leaving that transport, otherwise the relay
            # never reaches upstream subprocess cleanup.
            await down_write.aclose()
            await up_write.aclose()


def main() -> None:
    """Run the relay with its process-local SDK cleanup grace period."""
    # The outer client grants this relay two seconds after EOF. Its own child
    # gets a shorter grace period, avoiding competing two-second shutdowns.
    # This SDK setting is isolated to the dedicated relay subprocess.
    import mcp.client.stdio as sdk_stdio

    sdk_stdio.PROCESS_TERMINATION_TIMEOUT = 0.25
    anyio.run(relay, sys.argv[1])


if __name__ == "__main__":
    main()
