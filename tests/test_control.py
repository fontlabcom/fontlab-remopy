# this_file: tests/test_control.py
# SPDX-License-Identifier: Apache-2.0
"""Public ergonomic APIs, isolation and real persistent SDK lifetime."""

import asyncio
import sys

import pytest

from fontlab_remopy import (
    AsyncFontLab,
    FontLab,
    NativeExecutionError,
    ResultTransportError,
)
from fontlab_remopy.results import decode_execution, encode_execution


def execute_locally(source, variables):
    import contextlib
    import io

    code, nonce = encode_execution(source, variables, "sample.vfpy")
    output = io.StringIO()
    host = {"host_secret": 42}
    before = dict(host)
    with contextlib.redirect_stdout(output):
        exec(code, host)  # noqa: S102 - exercise the actual transmitted source in isolation
    assert host.keys() - before.keys() == {"__builtins__"}, "remote helper leaked names"
    return decode_execution({"success": True, "output": output.getvalue()}, nonce)


def test_json_variables_unicode_stdout_stderr_and_file_context():
    result = execute_locally(
        "import sys\nprint(value)\nprint('warning',file=sys.stderr)\nresult={'answer':value,'file':__file__}",
        {"value": 'Łódź ☃ " \\ $()'},
    )
    assert result.value["answer"] == 'Łódź ☃ " \\ $()'
    assert result.value["file"] == "sample.vfpy"
    assert result.stdout.startswith("Łódź ☃") and result.stderr == "warning\n"


def test_execution_errors_keep_traceback_and_partial_output():
    with pytest.raises(NativeExecutionError) as caught:
        execute_locally("print('before')\nraise ValueError('Łódź')", {})
    assert caught.value.payload["stdout"] == "before\n"
    assert "sample.vfpy" in caught.value.payload["error"]["traceback"]
    assert "ValueError" in str(caught.value)


@pytest.mark.parametrize("separator", ["\u0085", "\u2028", "\u2029"])
def test_json_line_separators_preserve_value_and_both_streams(separator):
    text = "before" + separator + "after"
    completed = execute_locally(
        "import sys\nprint(text)\nprint(text, file=sys.stderr)\nresult=text",
        {"text": text},
    )
    assert completed.value == text, "Unicode separator changed in returned value"
    assert completed.stdout == text + "\n", "Unicode separator changed in stdout"
    assert completed.stderr == text + "\n", "Unicode separator changed in stderr"


@pytest.mark.parametrize("separator", ["\u0085", "\u2028", "\u2029"])
def test_json_line_separators_preserve_native_exception_and_partial_streams(separator):
    text = "before" + separator + "after"
    with pytest.raises(NativeExecutionError) as caught:
        execute_locally(
            "import sys\nprint(text)\nprint(text, file=sys.stderr)\nraise ValueError(text)",
            {"text": text},
        )
    payload = caught.value.payload
    assert payload["error"]["message"] == text, "Native exception message changed"
    assert text in payload["error"]["traceback"], "Native traceback lost separator"
    assert payload["stdout"] == text + "\n", "Partial stdout changed"
    assert payload["stderr"] == text + "\n", "Partial stderr changed"


@pytest.mark.parametrize(
    "output, message",
    [
        ("random", "missing"),
        ('FONTLAB_REMOPY_nonce:{}\nFONTLAB_REMOPY_nonce:{}\n', "ambiguous"),
        ('FONTLAB_REMOPY_nonce:{"nonce":', "Incomplete remote JSON"),
    ],
)
def test_invalid_result_envelopes_fail_without_guessing(output, message):
    with pytest.raises(ResultTransportError, match=message):
        decode_execution({"success": True, "output": output}, "nonce")


def test_oversized_result_envelope_fails_explicitly():
    with pytest.raises(ResultTransportError, match="65536"):
        execute_locally("result='x' * 65536", {})


@pytest.mark.asyncio
async def test_result_decode_failure_never_replays_operation(monkeypatch):
    calls = []
    fl = AsyncFontLab()

    async def tool(name, arguments):
        calls.append((name, arguments))
        return {"success": True, "output": "missing envelope"}

    monkeypatch.setattr(fl, "_tool", tool)
    with pytest.raises(ResultTransportError, match="missing"):
        await fl.run("result=42")
    assert len(calls) == 1, "Already executed operation was replayed on decode failure"
    assert calls[0][0] == "run_python", "Wrong native operation submitted"


def test_unsupported_results_input_names_nan_and_limit_fail_clearly():
    with pytest.raises(ResultTransportError, match="serializ"):
        execute_locally("result=object()", {})
    for values in [{"bad-name": 1}, {"__builtins__": {}}, {"x": float("nan")}]:
        with pytest.raises((ValueError, TypeError)):
            encode_execution("pass", values, "<remote>")
    with pytest.raises(ValueError, match="32768"):
        encode_execution("x" * 32768, {}, "<remote>")
    with pytest.raises(ResultTransportError, match="missing"):
        decode_execution({"success": True, "output": "random"}, "nonce")


@pytest.fixture
def executing_bridge(tmp_path):
    path = tmp_path / "executing bridge"
    source = """try:
    from mcp.server.mcpserver import MCPServer as FastMCP
except ImportError:
    from mcp.server.fastmcp import FastMCP
import contextlib,io,json,os
from pathlib import Path
mcp=FastMCP('control fixture')
@mcp.tool()
def list_fonts():
    return {'fonts':[{'id':os.getpid(),'family_name':'Fixture'}]}
@mcp.tool()
def run_python(code:str):
    output=io.StringIO()
    with contextlib.redirect_stdout(output): exec(code,{})
    return json.dumps({'success':True,'output':output.getvalue()})
mcp.run(transport='stdio')
"""
    path.write_text("#!" + sys.executable + "\n" + source)
    path.chmod(0o755)
    return str(path)


def test_sync_reuses_connection_after_idle_and_closes(executing_bridge):
    import os
    import time

    fl = FontLab(command=executing_bridge, timeout=5)
    with fl:
        fl._async.timeout = 0.3
        pid = fl.list_fonts()["fonts"][0]["id"]
        time.sleep(0.35)
        assert fl.list_fonts()["fonts"][0]["id"] == pid, "idle timeout replaced session"
        assert fl.eval("a+2", a=40) == 42
        assert fl.run("print('ok'); result=[1,2]").stdout == "ok\n"
    with pytest.raises(ProcessLookupError):
        os.kill(pid, 0)
    with pytest.raises(RuntimeError, match="[Cc]onnect"):
        fl.eval("42")


@pytest.mark.asyncio
async def test_sync_inside_running_event_loop_and_async_equivalent(executing_bridge):
    with FontLab(command=executing_bridge) as fl:
        assert fl.eval("word", word="ą") == "ą"
    async with AsyncFontLab(command=executing_bridge) as fl:
        assert await fl.eval("40+2") == 42
        assert (await fl.run("result=None")).value is None
        with pytest.raises(NativeExecutionError):
            await fl.run("raise RuntimeError('native')")
        assert await fl.eval("42") == 42, "Python exception poisoned live connection"


def remote_add(value: int, amount: int = 2):
    """Remote callable with native-independent imports in its own body."""
    import math

    return {"answer": math.floor(value + amount)}


def remote_args(value=42):
    return value


def test_decorated_python_signature_defaults_and_return(executing_bridge):
    with FontLab(command=executing_bridge) as fl:
        remote = fl.python(remote_add)
        assert remote(40) == {"answer": 42}
        assert remote(value=39, amount=3) == {"answer": 42}
        assert remote.__name__ == "remote_add"
        assert fl.python(remote_args)() == 42, (
            "function name collided with argument transport"
        )
        with pytest.raises(TypeError):
            remote()
        captured = 42

        def closure():
            return captured

        with pytest.raises(ValueError, match="capture"):
            fl.python(closure)


def test_call_timeout_marks_outcome_unknown_blocks_reuse_and_reaps_process(
    executing_bridge,
):
    import os

    with FontLab(command=executing_bridge) as fl:
        pid = fl.list_fonts()["fonts"][0]["id"]
        fl._async.timeout = 0.1
        with pytest.raises(TimeoutError) as caught:
            fl.run("import time; time.sleep(2); result=42")
        assert any("unknown" in note for note in caught.value.__notes__)
        with pytest.raises(RuntimeError, match="fresh"):
            fl.eval("42")
    with pytest.raises(ProcessLookupError):
        os.kill(pid, 0)
    fl._async.timeout = 5
    with fl:
        assert fl.eval("42") == 42, "reopen must use a new portal/session/lock"


@pytest.mark.asyncio
async def test_async_cancel_propagates_and_reaps_process(executing_bridge):
    import os

    async with AsyncFontLab(command=executing_bridge) as fl:
        pid = (await fl.list_fonts())["fonts"][0]["id"]
        task = asyncio.create_task(fl.run("import time; time.sleep(2)"))
        await asyncio.sleep(0.05)
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task
        with pytest.raises(RuntimeError, match="fresh"):
            await fl.eval("42")
    with pytest.raises(ProcessLookupError):
        os.kill(pid, 0)


@pytest.mark.asyncio
async def test_queued_call_is_fenced_after_timeout_and_context_can_reopen(
    executing_bridge,
):
    fl = AsyncFontLab(command=executing_bridge)
    async with fl:
        fl.timeout = 0.1
        first = asyncio.create_task(fl.run("import time; time.sleep(2)"))
        await asyncio.sleep(0.01)
        queued = asyncio.create_task(fl.list_fonts())
        with pytest.raises(TimeoutError):
            await first
        with pytest.raises(RuntimeError, match="fresh"):
            await queued
    fl.timeout = 5
    async with fl:
        assert (await fl.fonts())[0]["family_name"] == "Fixture"


def test_native_exception_escaping_context_keeps_its_public_type(executing_bridge):
    with (
        pytest.raises(NativeExecutionError, match="broken"),
        FontLab(command=executing_bridge) as fl,
    ):
        fl.run("raise ValueError('broken')")
