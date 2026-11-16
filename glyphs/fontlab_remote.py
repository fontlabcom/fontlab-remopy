#MenuTitle: FontLab Remote Control
# this_file: glyphs/fontlab_remote.py
# SPDX-License-Identifier: Apache-2.0
__doc__ = """
Control a running FontLab 9 from Glyphs 3 or 4 (or any Python 3.8+), stdlib only.

Run from the Script menu: prints FontLab's open fonts and its version next to
Glyphs' current font, read-only. Import it from other Glyphs scripts:

    from fontlab_remote import FontLabClient
    with FontLabClient() as fl:
        print(fl.call("list_fonts"))
        print(fl.eval("2 + 40"))

FontLab must run with external MCP clients enabled (Preferences > Aidus).
The script starts FontLab's bundled ``fontlab-mcp`` bridge, which owns the
authentication for FontLab's local server, and speaks MCP JSON-RPC over its
standard input/output. Every read has a deadline, so Glyphs never hangs.
"""

import json
import os
import select
import subprocess
import tempfile
import time
import uuid

BRIDGES = (
    "/Applications/FontLab 9.app/Contents/MacOS/fontlab-mcp",
    os.path.expanduser("~/Applications/FontLab 9.app/Contents/MacOS/fontlab-mcp"),
)
PROTOCOL = "2024-11-05"


class FontLabError(RuntimeError):
    """FontLab, its bridge or a tool reported an error, or a deadline passed."""


def find_bridge():
    """``FONTLAB_MCP_COMMAND`` or the bridge inside an installed FontLab 9."""
    override = os.environ.get("FONTLAB_MCP_COMMAND")
    candidates = [override] if override else BRIDGES
    for path in candidates:
        if path and os.access(path, os.X_OK):
            return path
    raise FontLabError("FontLab 9's fontlab-mcp bridge was not found; set FONTLAB_MCP_COMMAND")


class FontLabClient:
    """One MCP session with FontLab. Use as a context manager, or call close()."""

    def __init__(self, command=None, timeout=15.0):
        if isinstance(command, str) or command is None:
            command = [command or find_bridge()]
        self.timeout = timeout
        self._next_id = 0
        self._buffer = b""
        self._stderr = tempfile.TemporaryFile()  # noqa: SIM115 - session owns this file until close(); a pipe could stall the bridge
        self._process = subprocess.Popen(
            list(command), stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=self._stderr, bufsize=0,
        )
        # Writes poll for room with the request deadline, so a bridge that
        # stops reading can't block Glyphs inside write().
        os.set_blocking(self._process.stdin.fileno(), False)
        try:
            self.server = self.request("initialize", {
                "protocolVersion": PROTOCOL,
                "capabilities": {},
                "clientInfo": {"name": "glyphs-fontlab-remote", "version": "1"},
            })
            self._send({"jsonrpc": "2.0", "method": "notifications/initialized"},
                       time.monotonic() + self.timeout)
        except BaseException:
            self.close()
            raise

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    def close(self):
        """End the session; the bridge exits when its input closes."""
        process = self._process
        try:
            process.stdin.close()  # always: the child may have exited already
        except OSError:
            pass
        if process.poll() is None:
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
        process.stdout.close()
        self._stderr.close()

    def _send(self, message, deadline):
        """Write one JSON line, all of it, before ``deadline``."""
        data = memoryview((json.dumps(message, ensure_ascii=False) + "\n").encode("utf-8"))
        fd = self._process.stdin.fileno()
        while data:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise FontLabError(f"FontLab bridge could not send within {float(self.timeout):.1f} s")
            _, ready, _ = select.select([], [fd], [], remaining)
            if not ready:
                continue
            try:
                data = data[os.write(fd, data):]
            except BlockingIOError:
                continue
            except OSError as error:
                raise FontLabError(f"FontLab bridge closed its input: {error!s}")

    def _readline(self, deadline):
        fd = self._process.stdout.fileno()
        while b"\n" not in self._buffer:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise FontLabError(f"No answer from FontLab within {float(self.timeout):.1f} s")
            ready, _, _ = select.select([fd], [], [], remaining)
            if not ready:
                continue
            chunk = os.read(fd, 65536)
            if not chunk:
                self._stderr.seek(0)
                detail = self._stderr.read().decode("utf-8", "replace").strip()
                raise FontLabError("FontLab bridge exited" + (": " + detail if detail else ""))
            self._buffer += chunk
        line, self._buffer = self._buffer.split(b"\n", 1)
        return line

    def request(self, method, params=None):
        """Send one JSON-RPC request and return its result.

        One deadline covers sending and the answer. Server notifications are
        ignored; server requests are answered (``ping``) or refused (anything
        else), never mistaken for the reply even when they reuse its id.
        """
        deadline = time.monotonic() + self.timeout
        self._next_id += 1
        ident = self._next_id
        self._send({"jsonrpc": "2.0", "id": ident, "method": method, "params": params or {}}, deadline)
        while True:
            line = self._readline(deadline).strip()
            if not line:
                continue
            message = json.loads(line.decode("utf-8"))
            if "method" in message:
                if "id" in message:
                    self._answer(message, deadline)
                continue
            if message.get("id") != ident:
                continue
            if "error" in message:
                error = message["error"]
                raise FontLabError(f"{error.get('message')!s} (code {error.get('code')!s})")
            return message.get("result", {})

    def _answer(self, message, deadline):
        """Reply to a server request: ping is answered, others are not supported."""
        if message["method"] == "ping":
            reply = {"jsonrpc": "2.0", "id": message["id"], "result": {}}
        else:
            reply = {"jsonrpc": "2.0", "id": message["id"],
                     "error": {"code": -32601, "message": "Method not supported: " + str(message["method"])}}
        self._send(reply, deadline)

    def tools(self):
        """FontLab's tool catalogue: a list of {name, description, inputSchema}."""
        tools, cursor = [], None
        while True:
            page = self.request("tools/list", {"cursor": cursor} if cursor else {})
            tools += page.get("tools", [])
            cursor = page.get("nextCursor")
            if not cursor:
                return tools

    def call(self, name, **arguments):
        """Call a FontLab tool; JSON text results are decoded. Tool errors raise."""
        result = self.request("tools/call", {"name": name, "arguments": arguments})
        texts = [item.get("text", "") for item in result.get("content", []) if item.get("type") == "text"]
        if result.get("isError"):  # FontLab sends isError: null on success
            raise FontLabError(f"FontLab tool {name!s} failed: {' '.join(texts)}")
        if not texts and result.get("structuredContent") is not None:
            return result["structuredContent"]
        values = []
        for text in texts:
            try:
                values.append(json.loads(text))
            except ValueError:
                values.append(text)
        return values[0] if len(values) == 1 else values

    def run_python(self, code):
        """Run code in FontLab (5-second host deadline); returns its output text."""
        payload = self.call("run_python", code=code)
        if isinstance(payload, dict) and "success" in payload:
            if not payload["success"]:
                raise FontLabError(f"FontLab Python failed: {payload.get('error', payload)!s}")
            return payload.get("output", "")
        return payload

    def eval(self, expression):
        """Evaluate a Python expression in FontLab and return its JSON value."""
        marker = f"GLYPHS_FONTLAB_{uuid.uuid4().hex}:"
        output = self.run_python(f"import json as _json\nprint({marker!r} + _json.dumps(({expression!s}), ensure_ascii=False))")
        for line in output.split("\n"):
            if line.startswith(marker):
                return json.loads(line[len(marker):])
        raise FontLabError(f"FontLab returned no value for {expression!r}: {output.strip()}")


def glyphs_font_name():
    """Glyphs' current font family name, or None outside Glyphs / without a font."""
    try:
        from GlyphsApp import Glyphs
    except ImportError:
        return None
    font = Glyphs.font
    return font.familyName if font is not None else None


def main():
    with FontLabClient() as fl:
        version = fl.eval("__import__('PythonQt').QtGui.QApplication.instance().applicationVersion")
        fonts = fl.call("list_fonts").get("fonts", [])
        print(f"FontLab {version!s} (MCP server {fl.server.get('serverInfo', {}).get('name', '?')!s})")
        print(f"FontLab open fonts: {len(fonts):d}")
        for font in fonts:
            print(f"  - {font.get('family_name', '?')!s} {font.get('style_name', '')!s}")
        print(f"FontLab says 2 + 40 = {fl.eval('2 + 40')!s}")
    print(f"Glyphs current font: {glyphs_font_name()!s}")


if __name__ == "__main__":
    main()
