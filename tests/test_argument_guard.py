# this_file: tests/test_argument_guard.py
# SPDX-License-Identifier: Apache-2.0
"""Unknown tool argument names are refused client-side; FontLab would drop them silently."""

import json

import pytest
from mcp.types import CallToolResult, ListToolsResult, Tool

from fontlab_remopy import AsyncFontLab


def _tool(name, schema):
    return Tool(name=name, inputSchema=schema)


STRICT = {"type": "object", "properties": {"font_id": {}, "master_name": {}}}
CATALOGUE = [
    _tool("list_kerning_pairs", STRICT),
    _tool("open_schema", {"type": "object", "properties": {"a": {}}, "additionalProperties": True}),
    _tool("no_props", {"type": "object"}),
    _tool("any_schema", {"type": "object", "properties": {"a": {}}, "additionalProperties": {}}),
]


class Session:
    def __init__(self):
        self.listed, self.called = 0, []

    async def list_tools(self, params=None):
        self.listed += 1
        return ListToolsResult(tools=CATALOGUE)

    async def call_tool(self, name, arguments=None):
        self.called.append((name, arguments))
        text = json.dumps({"ok": True})
        return CallToolResult.model_validate(
            {"content": [{"type": "text", "text": text}], "isError": False}
        )


def connected(session):
    client = AsyncFontLab()
    client._session = session
    return client


async def test_tool_when_unknown_argument_then_refused_naming_it_and_nothing_sent():
    session = Session()
    with pytest.raises(ValueError) as caught:
        await connected(session).tool("list_kerning_pairs", font_id=1, master="Bold")
    message = str(caught.value)
    assert "master" in message and "master_name" in message, message
    assert session.called == [], "a refused call must not reach FontLab"


async def test_tool_when_known_arguments_then_sent_and_catalogue_listed_once():
    session = Session()
    client = connected(session)
    for _ in range(2):
        await client.tool("list_kerning_pairs", font_id=1, master_name="Bold")
    assert len(session.called) == 2, "known arguments must pass"
    assert session.listed == 1, "catalogue must be fetched once per connection"


async def test_tool_when_tool_missing_from_catalogue_then_unchecked():
    session = Session()
    await connected(session).tool("brand_new_tool", anything=1)
    assert session.called == [("brand_new_tool", {"anything": 1})]


@pytest.mark.parametrize("name", ["open_schema", "no_props", "any_schema"])
async def test_tool_when_schema_open_or_without_properties_then_unchecked(name):
    session = Session()
    await connected(session).tool(name, whatever=1)
    assert session.called == [(name, {"whatever": 1})]


async def test_run_when_python_executed_then_catalogue_not_fetched():
    session = Session()
    client = connected(session)
    # run_python is internal and fixed-shape: no extra catalogue round trip.
    with pytest.raises(Exception):  # noqa: B017 - fake returns no execution envelope
        await client.run("result = 1")
    assert session.listed == 0


@pytest.fixture
def one_shot(monkeypatch):
    """Route fontlab_remopy.mcp's one-shot session to the fake."""
    from contextlib import asynccontextmanager

    import fontlab_remopy.mcp as mcp_api

    session = Session()

    @asynccontextmanager
    async def fake(command, timeout):
        yield session

    monkeypatch.setattr(mcp_api, "_session", fake)
    return mcp_api, session


async def test_call_tool_when_unknown_argument_then_refused_and_nothing_sent(one_shot):
    mcp_api, session = one_shot
    with pytest.raises(ValueError, match="master_name"):
        await mcp_api.call_tool("list_kerning_pairs", {"font_id": 1, "master": "Bold"})
    assert session.called == [], "a refused one-shot call must not reach FontLab"


async def test_call_tool_when_known_arguments_then_sent(one_shot):
    mcp_api, session = one_shot
    await mcp_api.call_tool("list_kerning_pairs", {"font_id": 1, "master_name": "Bold"})
    assert session.called == [("list_kerning_pairs", {"font_id": 1, "master_name": "Bold"})]


async def test_run_python_one_shot_when_called_then_catalogue_not_fetched(one_shot):
    mcp_api, session = one_shot
    with pytest.raises(RuntimeError):  # fake returns no execution envelope
        await mcp_api.run_python("result = 1")
    assert session.listed == 0, "run_python is fixed-shape; no catalogue round trip"
