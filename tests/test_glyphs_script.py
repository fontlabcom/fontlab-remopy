# this_file: tests/test_glyphs_script.py
# SPDX-License-Identifier: Apache-2.0
"""The stdlib-only Glyphs script speaks MCP to a real SDK server and keeps deadlines."""

import importlib.util
import json
import subprocess
import sys
import time
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "mcp_server.py"


def load():
    spec = importlib.util.spec_from_file_location("fontlab_remote", ROOT / "glyphs" / "fontlab_remote.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def remote(tmp_path, monkeypatch):
    monkeypatch.setenv("AIDUS_MCP_TEST_LOG", str(tmp_path / "log.txt"))
    return load()


def test_script_when_imported_then_stdlib_only():
    code = (
        "import sys, importlib.util; before = set(sys.modules);"
        f"spec = importlib.util.spec_from_file_location('r', {str(ROOT / 'glyphs' / 'fontlab_remote.py')!r});"
        "m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m);"
        "import sysconfig, os; std = sysconfig.get_paths()['stdlib'];"
        "bad = [n for n in set(sys.modules) - before if getattr(sys.modules[n], '__file__', None)"
        " and 'site-packages' in sys.modules[n].__file__];"
        "assert not bad, bad"
    )
    subprocess.run([sys.executable, "-I", "-c", code], check=True)


def test_client_when_fixture_server_then_tools_and_calls(remote, tmp_path):
    with remote.FontLabClient([sys.executable, str(FIXTURE)], timeout=20) as fl:
        assert fl.server["serverInfo"]["name"] == "FontLab fixture"
        assert {"list_fonts", "run_python"} <= {t["name"] for t in fl.tools()}
        assert fl.call("list_fonts") == {"id": "fixture-font", "family": "Fixture"}
        assert fl.call("run_python", code="print(1)") == "print(1)"
    assert (tmp_path / "log.txt").read_text() == "list_fonts called"


def test_client_when_tool_error_then_raises_with_message(remote):
    with remote.FontLabClient([sys.executable, str(FIXTURE)], timeout=20) as fl:
        with pytest.raises(remote.FontLabError, match="no_such_tool"):
            fl.call("no_such_tool")
        with pytest.raises(remote.FontLabError):
            fl.request("no/such/method")


def test_client_when_bridge_silent_then_deadline_and_cleanup(remote):
    started = time.monotonic()
    with pytest.raises(remote.FontLabError, match="No answer"):
        remote.FontLabClient([sys.executable, "-c", "import time; time.sleep(60)"], timeout=0.5)
    assert time.monotonic() - started < 5


def test_client_when_bridge_exits_then_error_includes_stderr(remote):
    command = [sys.executable, "-c", "import sys; sys.stderr.write('Cannot connect to FontLab 9'); sys.exit(1)"]
    with pytest.raises(remote.FontLabError, match="Cannot connect to FontLab 9"):
        remote.FontLabClient(command, timeout=5)


def test_call_when_null_is_error_then_success(remote):
    class Fake(remote.FontLabClient):
        def __init__(self):
            pass

        def request(self, method, params=None):
            return {"isError": None, "content": [{"type": "text", "text": '{"success": true, "output": "X:1\\n"}'}]}

    fake = Fake()
    assert fake.run_python("x") == "X:1\n"


def test_eval_when_marker_line_then_json_value(remote):
    class Fake(remote.FontLabClient):
        def __init__(self):
            pass

        def run_python(self, code):
            marker = code.split("print(")[1].split("'")[1]
            return "noise\n" + marker + '{"a": [1, "\\u0141"]}\n'

    assert Fake().eval("x") == {"a": [1, "Ł"]}


def test_find_bridge_when_override_missing_then_error(remote, monkeypatch):
    monkeypatch.setenv("FONTLAB_MCP_COMMAND", "/nonexistent/fontlab-mcp")
    with pytest.raises(remote.FontLabError, match="not found"):
        remote.find_bridge()


BRIDGE = r'''
import json, sys, time
log = open(sys.argv[1], "a")
def send(message):
    sys.stdout.write(json.dumps(message) + "\n"); sys.stdout.flush()
init = json.loads(sys.stdin.readline())
send({"jsonrpc": "2.0", "id": init["id"], "result": {"serverInfo": {"name": "fake"}}})
sys.stdin.readline()  # notifications/initialized
mode = sys.argv[2]
if mode == "stall":
    time.sleep(60)
if mode == "exit":
    sys.exit(0)
request = json.loads(sys.stdin.readline())
# Server-initiated requests reusing the client's id, before the real reply.
send({"jsonrpc": "2.0", "id": request["id"], "method": "ping"})
send({"jsonrpc": "2.0", "id": "s1", "method": "sampling/createMessage", "params": {}})
send({"jsonrpc": "2.0", "method": "notifications/message", "params": {}})
for _ in range(2):
    log.write(sys.stdin.readline()); log.flush()
send({"jsonrpc": "2.0", "id": request["id"], "result": {"answer": 42}})
'''


def fake(tmp_path, mode):
    script = tmp_path / "bridge.py"
    script.write_text(BRIDGE, encoding="utf-8")
    return [sys.executable, str(script), str(tmp_path / "log.jsonl"), mode]


def test_request_when_server_pings_with_same_id_then_pong_and_real_result(remote, tmp_path):
    with remote.FontLabClient(fake(tmp_path, "ping"), timeout=10) as fl:
        assert fl.request("tools/list") == {"answer": 42}
    replies = [json.loads(line) for line in (tmp_path / "log.jsonl").read_text().splitlines()]
    assert replies[0] == {"jsonrpc": "2.0", "id": 2, "result": {}}
    assert replies[1]["id"] == "s1" and replies[1]["error"]["code"] == -32601


def test_send_when_bridge_stops_reading_then_deadline_not_hang(remote, tmp_path):
    fl = remote.FontLabClient(fake(tmp_path, "stall"), timeout=1)
    started = time.monotonic()
    with pytest.raises(remote.FontLabError, match="No answer|could not send"):
        fl.request("tools/call", {"blob": "x" * 2_000_000})
    assert time.monotonic() - started < 4
    fl.close()


def test_close_when_bridge_already_exited_then_streams_closed(remote, tmp_path):
    fl = remote.FontLabClient(fake(tmp_path, "exit"), timeout=5)
    fl._process.wait(timeout=5)
    fl.close()
    assert fl._process.stdin.closed and fl._process.stdout.closed


def test_eval_when_tuple_expression_then_json_list(remote):
    import contextlib
    import io

    class Local(remote.FontLabClient):
        def __init__(self):
            pass

        def run_python(self, code):
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                exec(code, {})  # noqa: S102 - the generated wrapper, run locally
            return out.getvalue()

    assert Local().eval("1, 2") == [1, 2]
    assert Local().eval("[x * 2 for x in range(3)]") == [0, 2, 4]
