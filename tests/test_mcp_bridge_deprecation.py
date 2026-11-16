# this_file: tests/test_mcp_bridge_deprecation.py
# SPDX-License-Identifier: Apache-2.0
"""The legacy relay entry point warns on stderr and keeps stdout free for MCP."""

import importlib
import os
import subprocess
import sys

import pytest

MESSAGE = "fontlab_remopy.mcp_bridge is deprecated; use fontlab_remopy.mcp.relay"


def run_bridge():
    """Run the legacy entry point the way a saved MCP config does, with default warning filters."""
    env = {k: v for k, v in os.environ.items() if k != "PYTHONWARNINGS"}
    return subprocess.run(
        [sys.executable, "-m", "fontlab_remopy.mcp_bridge"],
        capture_output=True,
        stdin=subprocess.DEVNULL,
        timeout=10,
        check=False,
        env=env,
    )


def test_bridge_when_imported_then_warns_and_keeps_relay_exports(monkeypatch):
    from fontlab_remopy.mcp import relay

    monkeypatch.delitem(sys.modules, "fontlab_remopy.mcp_bridge", raising=False)
    with pytest.warns(DeprecationWarning, match=MESSAGE):
        bridge = importlib.import_module("fontlab_remopy.mcp_bridge")
    assert (bridge.main, bridge.relay, bridge.normalize_result) == (
        relay.main,
        relay.relay,
        relay.normalize_result,
    ), "Legacy imports must stay identical to the canonical relay"


def test_bridge_when_run_as_module_then_warning_reaches_stderr_with_default_filters():
    result = run_bridge()
    stderr = result.stderr.decode()
    assert "DeprecationWarning: " + MESSAGE in stderr, stderr


def test_bridge_when_run_as_module_then_stdout_is_byte_clean():
    result = run_bridge()
    assert result.stdout == b"", (
        f"stdout carries MCP frames and must stay empty: {result.stdout!r}"
    )
    assert result.returncode == 1, result.stderr.decode()
