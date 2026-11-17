# this_file: src/fontlab_remopy/cli.py
# SPDX-License-Identifier: Apache-2.0
"""Explicit launch, verified script execution and native MCP operations."""
import argparse
import asyncio
import json
import subprocess
from pathlib import Path
from typing import Any


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--timeout',type=float,default=30)
    parser.add_argument('--bridge',help='Explicit native bridge executable')
    sub = parser.add_subparsers(dest='operation',required=True)
    for operation in ('launch', 'submit'):
        command = sub.add_parser(operation)
        if operation == 'submit':
            command.add_argument('path', type=Path)
        command.add_argument('--backend', choices=('macos', 'crossover', 'wine'), default='macos')
        command.add_argument('--executable', type=Path)
        command.add_argument('--wine', type=Path, help='Explicit Wine/CrossOver launcher')
        selector = command.add_mutually_exclusive_group()
        selector.add_argument('--bottle', help='CrossOver bottle in the standard macOS location')
        selector.add_argument('--prefix', type=Path, help='Existing ordinary Wine prefix')
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
        if _timed_out(error) and args.operation in {'setup', 'execute', 'call', 'launch', 'submit'}:
            detail += 'Execution outcome is unknown; verify before repeating.\n'
        for note in getattr(error, '__notes__', []):
            detail += note + '\n'
        parser.exit(1,detail)
    print(json.dumps(result,indent=2))
    return 0


def _timed_out(error: BaseException) -> bool:
    if isinstance(error, BaseExceptionGroup):
        return any(_timed_out(child) for child in error.exceptions)
    return isinstance(error, (TimeoutError, subprocess.TimeoutExpired))


async def _perform(args: argparse.Namespace) -> Any:
    from .mcp import call_tool, execute_script, probe_tools
    from .mcp.compat import wire
    from .setup import setup_mcp
    match args.operation:
        case 'launch' | 'submit':
            return _submit(args)
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


def _submit(args: argparse.Namespace) -> dict[str, Any]:
    from . import platforms
    from .platforms import crossover, wine

    options: dict[str, Any] = {'timeout': args.timeout}
    provider = platforms
    if args.backend == 'macos':
        if any(value is not None for value in (args.executable, args.wine, args.bottle, args.prefix)):
            raise ValueError('Wine options require an explicit crossover or wine backend')
    else:
        if args.executable is None or args.wine is None:
            raise ValueError('Wine backends require --executable and --wine')
        options.update(executable=args.executable, wine=args.wine)
        if args.backend == 'crossover':
            if not args.bottle or args.prefix is not None:
                raise ValueError('CrossOver requires --bottle and does not accept --prefix')
            provider = crossover
            options['bottle'] = args.bottle
        else:
            if args.prefix is None or args.bottle is not None:
                raise ValueError('Wine requires --prefix and does not accept --bottle')
            provider = wine
            options['prefix'] = args.prefix
    if args.operation == 'launch':
        provider.launch(**options)
        return {'launch_requested': True}
    result = provider.submit_script(args.path, **options)
    return {'path': str(result.path), 'execution_verified': result.execution_verified}
