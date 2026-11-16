# this_file: tests/test_deprecated_modules.py
# SPDX-License-Identifier: Apache-2.0
"""Remopy 2.0 removed the pre-1.2 module paths; their canonical modules remain.

The `mcp_bridge` entry point still exists with a warning (see
tests/test_mcp_bridge_deprecation.py) and goes one major later.
"""

import importlib
import pkgutil
import sys

import pytest

import fontlab_remopy

REMOVED = {
    "control": ("client", ("FontLab", "AsyncFontLab")),
    "controls": ("actions", ("Controls",)),
    "functions": ("remote", ("remote_function",)),
    "execution": (
        "results",
        ("ExecutionResult", "ResultTransportError", "encode_execution",
         "decode_execution", "MAX_CODE_BYTES", "MAX_OUTPUT_BYTES"),
    ),
    "native": ("host", ("enable_mcp",)),
    "mcp_api": (
        "mcp",
        ("NativeExecutionError", "bridge_parameters", "probe_tools",
         "call_tool", "run_python", "execute_script"),
    ),
    "mcp_compat": ("mcp.compat", ("field", "is_error", "next_cursor", "wire", "unwrap")),
    "launch_api": (
        "platforms",
        ("ScriptSubmission", "find_bridge", "launch", "submit_script", "DEFAULT_APP"),
    ),
}


@pytest.mark.parametrize("old", sorted(REMOVED))
def test_old_module_when_imported_then_raises_module_not_found(old, monkeypatch):
    monkeypatch.delitem(sys.modules, "fontlab_remopy." + old, raising=False)
    with pytest.raises(ModuleNotFoundError) as caught:
        importlib.import_module("fontlab_remopy." + old)
    assert caught.value.name == "fontlab_remopy." + old, caught.value


@pytest.mark.parametrize("old", sorted(REMOVED))
def test_old_module_when_listed_then_absent_from_package(old):
    present = {info.name for info in pkgutil.iter_modules(fontlab_remopy.__path__)}
    assert old not in present, f"{old}.py must not ship in 2.0"


@pytest.mark.parametrize("old", sorted(REMOVED))
def test_migration_target_when_imported_then_provides_every_moved_name(old):
    new, names = REMOVED[old]
    target = importlib.import_module("fontlab_remopy." + new)
    missing = [name for name in names if not hasattr(target, name)]
    assert not missing, f"fontlab_remopy.{new} lost {missing} (migration for {old})"


def test_bridge_when_listed_then_still_ships_until_next_major():
    present = {info.name for info in pkgutil.iter_modules(fontlab_remopy.__path__)}
    assert "mcp_bridge" in present, "mcp_bridge is removed one major after 2.0"
