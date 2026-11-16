# this_file: tests/test_discovery.py
# SPDX-License-Identifier: Apache-2.0
"""Portable discovery preserves override priority, spaces and bundle fallback."""

import pytest

from fontlab_remopy import discovery


@pytest.mark.parametrize(
    "command,primary,legacy,expected",
    [
        ("explicit bridge", "primary bridge", "legacy bridge", "explicit bridge"),
        (None, "primary bridge", "legacy bridge", "primary bridge"),
        (None, "", "legacy bridge", "legacy bridge"),
    ],
)
def test_override_when_set_then_only_highest_priority_command_is_used(
    monkeypatch, command, primary, legacy, expected
):
    monkeypatch.setenv("FONTLAB_MCP_COMMAND", primary)
    monkeypatch.setenv("AIDUS_FONTLAB_MCP_COMMAND", legacy)
    calls = []
    monkeypatch.setattr(discovery.shutil, "which", lambda value: calls.append(value) or value)
    assert discovery.find_bridge(command) == expected
    assert calls == [expected], "Do not split commands containing spaces or try fallbacks"


@pytest.mark.parametrize("candidate", ["path", "bundle", "home", "missing"])
def test_discovery_when_no_override_then_checks_path_and_bundles(monkeypatch, candidate):
    monkeypatch.delenv("FONTLAB_MCP_COMMAND", raising=False)
    monkeypatch.delenv("AIDUS_FONTLAB_MCP_COMMAND", raising=False)
    path = "/tools/fontlab-mcp"
    bundle = str(discovery.DEFAULT_APP / "Contents/MacOS/fontlab-mcp")
    home = str(discovery.Path.home() / "Applications/FontLab 9.app/Contents/MacOS/fontlab-mcp")
    expected = {"path": path, "bundle": bundle, "home": home, "missing": None}[candidate]
    monkeypatch.setattr(discovery.shutil, "which", lambda _: path if candidate == "path" else None)
    monkeypatch.setattr(discovery.os, "access", lambda value, mode: value == expected)
    assert discovery.find_bridge() == expected
