---
this_file: src_docs/md/api-and-glyphs-cli.md
---

# API, sessions and command line


| Name | What it does |
| --- | --- |
| `FontLab(command=None, timeout=30)` | Synchronous client; use as `with FontLab() as fl:`. `command` is the bridge executable, `timeout` seconds per call |
| `AsyncFontLab(command=None, timeout=30)` | Same operations as `async with` and `await` |
| `fl.run(code, **vars)` | Run Python in FontLab; returns `ExecutionResult(value, stdout, stderr)`; set `result` to return a value |
| `fl.eval(expression, **vars)` | Evaluate one expression; returns the JSON value |
| `fl.execute_script(path, **vars)` | Run a `.flpy`/`.vfpy` file, `__file__` set to its resolved path |
| `fl.tool(name, **arguments)` / `fl.tools()` | Call any native tool by name / list the live catalogue with schemas. Unknown argument names raise `ValueError` (FontLab would drop them silently); the master argument is `master_name` |
| `fl.fonts()`, `fl.output()`, named controls | Open fonts; recent captured output; the catalogue tools listed below |
| `@fl.python` | Run a decorated function remotely with JSON arguments and result |
| `enable_mcp()` | Inside FontLab: set `mcp.enabled` and notify the host (no `save()`) |
| `setup_mcp()`, `launch()`, `submit_script()`, `find_bridge()` | Launch FontLab, enable MCP from outside, locate the bridge |
| `call_tool()`, `run_python()`, `execute_script()`, `probe_tools()` | One-shot async functions for single calls |

Errors: `NativeExecutionError` (a tool or the remote Python failed; `.payload` has type,
message, traceback and partial output), `ResultTransportError` (the result could not be
recovered; the call may have run), `ValueError` (bad `timeout`, variable name or oversized
code), `FileNotFoundError` (no bridge executable), `RuntimeError` (used outside a context, or
after a timeout until you open a fresh one), and `TimeoutError` (the call exceeded `timeout`;
the outcome is unknown, so check FontLab before repeating).

Two different time limits apply. `timeout` is how long this client waits for one MCP call.
FontLab's `run_python` tool also enforces its own fixed five-second execution deadline,
which Remopy cannot change: code passed to `run`, `eval` or a `@fl.python` function must
finish within it, so split longer work into short calls and read the resulting state.
Remote code is limited to 32768 bytes and its output to 65536 bytes.

One context reuses one authenticated MCP connection. Idle time has no deadline;
each initialization/call has the configured `timeout` (30 seconds by default).
This synchronous API also works in notebooks with an existing event loop. It
owns a dedicated AnyIO portal thread and releases its bridge on context exit or
`close()`. `AsyncFontLab` exposes the same operations with `async with` and
`await`; enter and exit that context on the same task. Calls are serialized.
After timeout/cancellation, queued/new calls fail until a fresh context opens.
The original one-shot async functions (`call_tool`, `run_python`,
`execute_script`, `probe_tools`) retain their existing result shapes.

`run` returns `ExecutionResult(value, stdout, stderr)`; set `result` in ordinary
Python to return a value. `eval` returns the value directly. Context methods
`execute_script(path, **variables)` preserve the resolved filename. JSON data is
bound into an isolated namespace; `fontlab`, `fontgate`, `fontpr`, and `PythonQt`
are prebound when available. Explicit variables take precedence. Imports/names
from FontLab's global script scope are not inherited or changed. Python streams
are captured during execution; concurrent Python threads share those interpreter
streams. Native Output is never cleared.
Unicode text, including U+0085, U+2028 and U+2029, round-trips unchanged in
values, captured streams and native exception messages; only LF frames envelopes.

`@fl.python` preserves the local function signature and metadata, binds defaults
locally, and transports arguments/results as JSON. Put imports inside the body.
Globals/closures, async function bodies, unavailable source, native object
results, and non-JSON values fail clearly; notebook source limitations can use
`run`/`eval`. Native exceptions retain type/message/traceback and partial output
in `NativeExecutionError.payload`. Truncated/missing/unsupported JSON results
raise `ResultTransportError`. The wrapper counts toward native 32768-byte code
and 65536-byte output bounds; FontLab's fixed five-second execution deadline is
unchanged. A timeout leaves execution outcome unknown and never triggers retry.

Named controls include `fonts`, `current_font`, `current_glyphs`, `glyph("A")`,
`font_info`, `font_metrics`, `glyph_metrics`, `list_actions`, `run_actions`,
`output`, font open/new/save/close/activation and metric setters. Mutating calls
perform the requested native operation. `tool(name, **arguments)` accesses the
whole live catalogue; `tools()` gives its current schemas. `output()` reads MCP's
recent capture; `eval("fontlab.GetProperty('output')")` reads the full native
Output. The checkout provides `examples/control.py` for ordinary Python and `examples/native_smoke.py` for a read-only one-shot async check; their source is not rendered here.
App's native UI example
creates a native panel, modeless dialog and removable
Preview drawing from `@fl.python` functions; `--typerig` composes a real TypeRig
widget. Install Fontlabapp (and optionally typerig) in the host first. The example
retains its native handles across calls, waits outside the UI thread, and removes
only its own resources in `finally`.

`execute_script()` reads .flpy/.vfpy source, preserves its resolved filename as
__file__, and verifies the native run_python success payload. Native errors raise
NativeExecutionError with the original payload. `call_tool()` returns the actual
SDK result, including real errors. FontLab's fixed execution deadline remains
unchanged. Timeouts leave a mutation's outcome unknown; operations are never
automatically retried.

`launch()` requests application launch. `submit_script()` uses file association
and returns execution_verified=False: submission alone cannot prove execution.
The library's launch/file-association implementation currently supports macOS;
MCP can use an explicitly configured executable on other supported SDK platforms.

`setup_mcp()` submits one unique .vfpy macro, verifies a nonce-matched native
completion marker, then authenticates the bridge and discovers the tool catalogue.
Only the extended mcp.enabled preference is set, using load() and a host
notification. Failed/timeout setup retains local macro/status files for inspection.
`enable_mcp()` performs the same preference update when called inside FontLab.
It does not call save() or clear application logs.

Discovery checks an explicit argument or FONTLAB_MCP_COMMAND, then the native
bridge on PATH or the FontLab 9 bundle. The legacy AIDUS_FONTLAB_MCP_COMMAND
variable remains accepted for migration. Paths containing spaces are preserved.
An explicit missing executable never falls back to a different FontLab build.

```sh
fontlab-remopy launch
fontlab-remopy --timeout 15 setup
fontlab-remopy tools
fontlab-remopy execute example.flpy
fontlab-remopy call list_fonts
```


## Remote-control FontLab from Glyphs


`glyphs/fontlab_remote.py` runs inside Glyphs 3 or 4 (or any Python 3.8+) with the
standard library only, so Glyphs' Python needs nothing installed. It starts FontLab's
bundled `fontlab-mcp` bridge (which holds the authentication for FontLab's local
server) and speaks MCP over its standard input/output, with a deadline on every read.

Install: copy the file into Glyphs' Scripts folder (Script > Open Scripts Folder,
i.e. `~/Library/Application Support/Glyphs 3/Scripts/`), then Script > Reload Scripts.
FontLab must be running with external MCP clients enabled (Preferences > Aidus).
Run **Script > FontLab Remote Control** to print FontLab's version and open fonts
next to Glyphs' current font in the Macro panel. From your own Glyphs scripts:

```python
from fontlab_remote import FontLabClient

with FontLabClient() as fl:
    print([t["name"] for t in fl.tools()])
    print(fl.call("list_fonts"))                  # any FontLab MCP tool
    print(fl.eval("2 + 40"))                      # a JSON value from FontLab Python
    fl.run_python("print(fontlab.CurrentFont())")  # output text
```

Tool errors, bridge exits (with the bridge's message) and missed deadlines raise
`FontLabError`. `FONTLAB_MCP_COMMAND` selects another bridge. Glyphs' Python must be
configured (Glyphs > Settings > Addons); a framework that no longer exists makes every
Glyphs script fail before this one starts.
