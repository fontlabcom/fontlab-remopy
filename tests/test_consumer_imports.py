# this_file: tests/test_consumer_imports.py
# SPDX-License-Identifier: Apache-2.0
"""Consumers' top-level imports stay in ``_EXPORTS`` (Issue 250, TODO rows 7 and 13).

App owns ``examples/native_ui.py``; it imports ``fontlab_remopy.FontLab`` and
drives it as a context manager with the ``python`` decorator. The App check
parses the sibling App checkout when present (source only; native use stays
an owner check).
"""

import ast
import inspect
from pathlib import Path

import pytest

import fontlab_remopy
from fontlab_remopy import client

# Top-level names other maintained repositories import (triage remopy-row7-scope).
CONSUMER_IMPORTS = (
    "FontLab",
    "enable_mcp",
    "find_bridge",
    "probe_tools",
    "bridge_parameters",
)
NATIVE_UI = (
    Path(__file__).resolve().parents[2]
    / "fontlab-fontlabapp"
    / "examples"
    / "native_ui.py"
)


@pytest.mark.parametrize("name", CONSUMER_IMPORTS)
def test_consumer_import_when_resolved_then_listed_and_lazy_exported(name):
    assert name in fontlab_remopy._EXPORTS, f"{name} must stay a top-level export"
    assert name in fontlab_remopy.__all__
    module = __import__(
        "fontlab_remopy." + fontlab_remopy._EXPORTS[name], fromlist=[name]
    )
    assert getattr(fontlab_remopy, name) is getattr(module, name)


def test_app_native_ui_when_parsed_then_its_remopy_names_and_calls_exist():
    if not NATIVE_UI.is_file():
        pytest.skip("App sibling checkout is not present")
    tree = ast.parse(NATIVE_UI.read_text())
    imported = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module == "fontlab_remopy"
        for alias in node.names
    }
    assert imported == {"FontLab"}, imported
    assert set(imported) <= set(fontlab_remopy._EXPORTS)
    remote = fontlab_remopy.FontLab
    assert remote is client.FontLab
    # native_ui calls RemoteFontLab() with no arguments and uses it as a context manager.
    parameters = inspect.signature(remote).parameters
    assert all(p.default is not inspect.Parameter.empty for p in parameters.values())
    assert callable(remote.__enter__) and callable(remote.__exit__)
    # Its helpers are decorated with ``@fl.python``.
    decorators = {
        d.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef)
        for d in node.decorator_list
        if isinstance(d, ast.Attribute)
        and isinstance(d.value, ast.Name)
        and d.value.id == "fl"
    }
    assert decorators == {"python"}, decorators
    assert list(inspect.signature(remote.python).parameters) == ["self", "function"]
    # native_ui applies it as a bare decorator, so ``function`` must accept a positional argument.
    assert inspect.signature(remote.python).parameters["function"].kind in (
        inspect.Parameter.POSITIONAL_ONLY,
        inspect.Parameter.POSITIONAL_OR_KEYWORD,
    )
