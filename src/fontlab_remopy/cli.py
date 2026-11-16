# this_file: src/fontlab_remopy/cli.py
# SPDX-License-Identifier: Apache-2.0
"""Explicit launch, verified script execution and native MCP operations."""
import argparse
import asyncio
import json
from pathlib import Path
from typing import Any


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--timeout',type=float,default=30)
    parser.add_argument('--bridge',help='Explicit native bridge executable')
    sub = parser.add_subparsers(dest='operation',required=True)
    sub.add_parser('launch')
    sub.add_parser('setup')
    sub.add_parser('tools')
    execute = sub.add_parser('execute')
    execute.add_argument('path',type=Path)
    call = sub.add_parser('call')
    call.add_argument('name')
    call.add_argument('--arguments',type=json.loads,default={})
    args = parser.parse_args(argv)
    try:
        result = asyncio.run(_perform(args))
    except Exception as error:  # noqa: BLE001 - CLI boundary reports any SDK or remote failure with exit status 1
        detail = f'{type(error).__name__}: {error}\n'
        if _timed_out(error) and args.operation in {'setup', 'execute', 'call'}:
            detail += 'Execution outcome is unknown; verify before repeating.\n'
        for note in getattr(error, '__notes__', []):
            detail += note + '\n'
        parser.exit(1,detail)
    print(json.dumps(result,indent=2))
    return 0


def _timed_out(error: BaseException) -> bool:
    if isinstance(error, BaseExceptionGroup):
        return any(_timed_out(child) for child in error.exceptions)
    return isinstance(error, TimeoutError)


async def _perform(args: argparse.Namespace) -> Any:
    from .mcp import call_tool, execute_script, probe_tools
    from .mcp.compat import wire
    from .platforms import launch
    from .setup import setup_mcp
    match args.operation:
        case 'launch':
            launch(timeout=args.timeout)
            return {'launch_requested':True}
        case 'setup':
            result = await setup_mcp(command=args.bridge,timeout=args.timeout)
            return {'execution_verified':result.execution_verified,'tools':len(result.tools)}
        case 'tools':
            return [wire(tool) for tool in await probe_tools(args.bridge,args.timeout)]
        case 'execute':
            return await execute_script(args.path,args.bridge,args.timeout)
        case 'call':
            return wire(await call_tool(args.name,args.arguments,args.bridge,args.timeout))
    raise ValueError('Unknown operation')
