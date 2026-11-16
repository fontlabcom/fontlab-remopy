# this_file: tests/test_api_surface.py
# SPDX-License-Identifier: Apache-2.0
"""Public client API against a fake session that runs the transmitted code locally; no FontLab."""

import asyncio
import contextlib
import io
import json

import pytest
from mcp.types import CallToolResult, ListToolsResult

from fontlab_remopy import AsyncFontLab, FontLab, NativeExecutionError
from fontlab_remopy.actions import Controls

NAMED = {
    "list_fonts": ("list_fonts", {}),
    "current_font": ("get_active_font", {}),
    "current_glyphs": ("get_current_glyphs", {}),
    "font_info": ("get_font_info", {"a": 1}),
    "glyph_info": ("get_glyph", {"a": 1}),
    "list_glyphs": ("list_glyphs", {"a": 1}),
    "font_metrics": ("get_font_metrics", {"a": 1}),
    "glyph_metrics": ("get_glyph_metrics", {"a": 1}),
    "list_actions": ("list_actions", {}),
    "run_actions": ("run_actions", {"a": 1}),
    "output": ("get_python_output", {"a": 1}),
    "open_font": ("open_font", {"a": 1}),
    "new_font": ("new_font", {"a": 1}),
    "save_font": ("save_font", {"a": 1}),
    "close_font": ("close_font", {"a": 1}),
    "activate_font": ("set_active_font", {"a": 1}),
    "activate_glyph": ("set_active_glyph", {"a": 1}),
    "set_font_metrics": ("set_font_metrics", {"a": 1}),
    "set_glyph_metrics": ("set_glyph_metrics", {"a": 1}),
}


class Recorder(Controls):
    def tool(self, name, **arguments):
        return name, arguments


@pytest.mark.parametrize("method", sorted(NAMED))
def test_controls_when_named_call_made_then_catalogue_tool_and_arguments_match(method):
    expected_tool, arguments = NAMED[method]
    assert getattr(Recorder(), method)(**arguments) == (expected_tool, arguments)


def test_controls_when_glyph_called_then_name_becomes_glyph_name_argument():
    assert Recorder().glyph("A", layer="x") == ("get_glyph", {"glyph_name": "A", "layer": "x"})


def _text(value):
    return {"content": [{"type": "text", "text": json.dumps(value)}], "isError": False}


class FakeSession:
    """Answers run_python by executing the transmitted code, like FontLab's tool."""

    def __init__(self, pages=(), delay=0):
        self.pages, self.delay, self.calls = list(pages), delay, []

    async def list_tools(self, params=None):
        # An unscripted catalogue is empty: the argument guard then has no schema to check.
        return self.pages.pop(0) if self.pages else ListToolsResult(tools=[])

    async def call_tool(self, name, arguments=None):
        self.calls.append(name)
        await asyncio.sleep(self.delay)
        if name == "run_python":
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                exec(arguments["code"], {})  # noqa: S102 - the code under test
            return CallToolResult.model_validate(_text({"success": True, "output": out.getvalue()}))
        if name == "boom":
            return CallToolResult.model_validate({"content": [], "isError": True})
        if name == "two":
            return CallToolResult.model_validate(
                {"content": [{"type": "text", "text": "1"}, {"type": "text", "text": "2"}], "isError": False}
            )
        if name == "list_fonts":
            return CallToolResult.model_validate(_text({"fonts": [{"family_name": "F"}]}))
        return CallToolResult.model_validate(_text({"name": name, "arguments": arguments}))


def connected(session, **kwargs):
    client = AsyncFontLab(**kwargs)
    client._session = session
    return client


def test_async_when_tools_paged_then_all_pages_are_collected():
    tool = {"name": "a", "inputSchema": {"type": "object"}}
    pages = [ListToolsResult.model_validate({"tools": [tool], "nextCursor": "n"}),
             ListToolsResult.model_validate({"tools": [{**tool, "name": "b"}]})]
    names = [t.name for t in asyncio.run(connected(FakeSession(pages)).tools())]
    assert names == ["a", "b"]


def test_async_when_run_eval_and_execute_script_then_values_and_streams_round_trip(tmp_path):
    async def scenario():
        client = connected(FakeSession())
        done = await client.run("print('hi'); result = n * 2", n=21)
        assert (done.value, done.stdout, done.stderr) == (42, "hi\n", "")
        assert await client.eval("n + 1", n=1) == 2
        script = tmp_path / "s.vfpy"
        script.write_text("result = __file__", encoding="utf-8")
        assert (await client.execute_script(script)).value == str(script.resolve())
        assert await client.fonts() == [{"family_name": "F"}]

    asyncio.run(scenario())


def test_async_when_tool_fails_or_returns_many_payloads_then_clear_errors():
    async def scenario():
        client = connected(FakeSession())
        with pytest.raises(NativeExecutionError):
            await client.tool("boom")
        with pytest.raises(RuntimeError, match="single JSON payload"):
            await client.tool("two")
        with pytest.raises(ValueError):
            await client.tool("x", bad=float("nan"))

    asyncio.run(scenario())


def test_async_when_not_connected_or_connected_twice_then_runtime_error():
    async def scenario():
        with pytest.raises(RuntimeError, match="fresh context"):
            await AsyncFontLab().tool("list_fonts")
        with pytest.raises(RuntimeError, match="already connected"):
            await connected(FakeSession()).__aenter__()

    asyncio.run(scenario())


@pytest.mark.parametrize("timeout", [0, -1, float("inf"), float("nan")])
def test_clients_when_timeout_not_positive_finite_then_value_error(timeout):
    with pytest.raises(ValueError, match="positive"):
        AsyncFontLab(timeout=timeout)


def test_async_when_call_times_out_then_outcome_unknown_and_later_calls_refused():
    async def scenario():
        client = connected(FakeSession(delay=1), timeout=0.01)
        with pytest.raises(TimeoutError) as caught:
            await client.tool("slow")
        assert any("outcome may be unknown" in n for n in caught.value.__notes__)
        with pytest.raises(RuntimeError, match="fresh context"):
            await client.tool("slow")

    asyncio.run(scenario())


def test_sync_when_used_outside_context_then_runtime_error_and_close_is_idempotent():
    client = FontLab()
    with pytest.raises(RuntimeError, match="with context"):
        client.fonts()
    client.close()
    client.close()


def test_sync_when_connected_flag_set_then_enter_refused():
    client = FontLab()
    client._stack = object()
    with pytest.raises(RuntimeError, match="already connected"):
        client.__enter__()


def test_sync_when_bridge_missing_then_enter_raises_and_resets(monkeypatch):
    monkeypatch.setattr("fontlab_remopy.client.find_bridge", lambda command: None)
    client = FontLab()
    with pytest.raises(BaseException) as caught:  # may arrive wrapped by the SDK task group
        client.__enter__()
    assert "No executable FontLab MCP bridge" in repr(caught.value)
    assert client._stack is None and client._portal is None


def test_sync_when_method_called_through_portal_then_it_reaches_async_client():
    client = FontLab()
    client._async = connected(FakeSession())
    from anyio.from_thread import start_blocking_portal

    with start_blocking_portal() as portal:
        client._portal = portal
        assert client.fonts() == [{"family_name": "F"}]
        assert client.eval("1 + 1") == 2
        assert client.tool("x", a=1)["name"] == "x"
        assert client.run("result = 3").value == 3
        client._portal = None
