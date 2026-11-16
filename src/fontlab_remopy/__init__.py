# this_file: src/fontlab_remopy/__init__.py
# SPDX-License-Identifier: Apache-2.0
"""Reusable FontLab remote control; imports remain light inside the host."""
from importlib import import_module
from typing import Any

_EXPORTS = {"launch":"platforms", "submit_script":"platforms", "ScriptSubmission":"platforms",
            "find_bridge":"platforms", "enable_mcp":"host", "setup_mcp":"setup",
            "bridge_parameters":"mcp", "probe_tools":"mcp", "call_tool":"mcp",
            "run_python":"mcp", "execute_script":"mcp", "NativeExecutionError":"mcp",
            "FontLab":"client", "AsyncFontLab":"client", "ExecutionResult":"results",
            "ResultTransportError":"results"}
__all__ = list(_EXPORTS)


def __getattr__(name: str) -> Any:
    if name not in _EXPORTS:
        raise AttributeError(name)
    value = getattr(import_module('.'+_EXPORTS[name],__name__),name)
    globals()[name] = value
    return value
