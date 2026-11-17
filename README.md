---
this_file: README.md
---

## Install in FontLab

To install into FontLab 9, open `install.vfpy` from a checkout in FontLab
(double-click it or drop it onto FontLab), then restart FontLab. The file is a
short stub that hands the work to
[fontlab-instamix](https://github.com/fontlabcom/fontlab-python-instamix); if
instamix is not installed yet, the stub installs it from PyPI first. Instamix
installs the package into FontLab's own `site-packages` and records the install
under the extension id `com.fontlab.remopy`.

## Development status — 2026-11-05

Canonical source inspected for this proposal: `33a03efbda44`. This is a dated source observation, not an installed or native acceptance claim.

Reconcile caller migrations and Issue 207 distribution changes without removing genuine supported-host or SDK compatibility.

Requalify installed launch/catalogue/nonce execution on the supported host and the App-owned native UI consumer; timeouts do not cancel host code.

## Repository and development

`src/fontlab_remopy/` contains clients, actions, discovery and MCP compatibility; `examples/`, `glyphs/` and `tests/` hold consumers and checks. App owns the relocated `examples/native_ui.py`.

Run `uv sync --extra test`, `./test.sh`, `uv run --extra test --with "mcp==1.30.0" python -m pytest -q`, and `uv run --extra test --with "mcp==1.26.0" python -m pytest -q`. All three lines are required for the advertised SDK range.

Keep runtime, ordinary installed artifacts, native workflows and published documentation as separate acceptance results. Track open checks in [TODO.md](TODO.md), the implementation route in [PLAN.md](PLAN.md), and dated evidence in [CHANGELOG.md](CHANGELOG.md).

# FontLab Remopy

`fontlab_remopy` controls FontLab remotely using native MCP and macOS application
launch/file association. Python 3.11+ is required. Agent prompts, role selection
and AI libraries belong to Aidus and are not dependencies here.

```python
from fontlab_remopy import FontLab

with FontLab() as fl:
    print(fl.fonts())
    answer = fl.eval("value + 2", value=40)
    families = fl.eval('[f["family_name"] for f in fontpr.list_fonts()["fonts"]]')
    completed = fl.run("print(message); result={'answer':42}", message="Łódź")
    print(completed.value, completed.stdout, completed.stderr)

    @fl.python
    def metrics(name: str):
        import fontpr
        return fontpr.get_glyph_metrics(glyph_name=name)

    # With an open font containing A:
    print(metrics("A"))
```

## CrossOver and Wine script submission

`submit` requests a script open and prints its resolved `path` with
`execution_verified: false`. It does not establish host readiness or completed
execution. `execute` retains authenticated native MCP execution. A launch or
submission timeout leaves the outcome unknown; inspect the host before repeating.
No operation retries automatically.

Choose the backend explicitly. CrossOver requires its existing standard macOS
`~/Library/Application Support/CrossOver/Bottles/NAME` bottle, a native executable
path inside that bottle's `drive_c`, and an executable CrossOver Wine launcher.
The validated absolute bottle selector avoids configured bottle search paths.
Scripts are existing native files and may be outside the bottle:

```sh
fontlab-remopy --timeout 10 submit ./probe.vfpy --backend crossover \
  --bottle fontlab --wine /Applications/CrossOver.app/Contents/SharedSupport/CrossOver/bin/wine \
  --executable "$HOME/Library/Application Support/CrossOver/Bottles/fontlab/drive_c/Program Files/Fontlab/FontLab 9/FontLab 9.exe"
```

For ordinary Wine, use `--backend wine --prefix /existing/prefix`, together with
`--wine /path/to/wine` and `--executable /existing/prefix/drive_c/path/FontLab.exe`.
Both executable and script must be inside that prefix's `drive_c`; no Z: mapping
is assumed. `launch` takes the same backend options without a script path.
Default macOS `launch` and `submit PATH` use the existing application provider.

Python callers can import `launch` and `submit_script` explicitly from
`fontlab_remopy.platforms.crossover` or `fontlab_remopy.platforms.wine`:
`submit_script(path, executable, bottle="fontlab", wine=launcher, timeout=10)`;
ordinary Wine uses `prefix=prefix_path` instead of `bottle`.
Paths, executable launcher permissions and finite positive deadlines are checked
before starting a process. These routes have offline command-construction tests;
actual Windows execution, Windows uv/Python bootstrap, installation and MCP
bridge availability still require separate native qualification.

## Documentation test environment

Documentation checks use a separate Python 3.13 environment, matching
`.github/workflows/docs.yml` and the Python 3.13 requirements lock. This is a
build contract, not a change to Remopy's Python 3.11 host requirement.
Use uv 0.13.7 and the exact locked dependencies:

```sh
uv venv --python 3.13 .docs-venv
uv pip install --python .docs-venv/bin/python --require-hashes -r src_docs/requirements.txt
PATH="$PWD/.docs-venv/bin:$PATH" sh src_docs/build.sh
PATH="$PWD/.docs-venv/bin:$PATH" python -m unittest discover -s tests_docs -v
```

Run the build before checking generated output. Do not use an unrelated global
MaterialX installation: the reviewed browser assets and search configuration
require `mkdocs-materialx==10.1.8`. MaterialX 10.2 changes those assets and the
search plugin configuration; updating the lock requires a separate asset and
licence review, not relaxed assertions. PySide6 is not FontLab's native
PythonQt environment; native checks use pythonqtside in FontLab.

## API reference

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
Output. See `examples/control.py` for runnable ordinary Python and `examples/native_smoke.py` for a read-only check of the one-shot async functions.
[App's native UI example](https://github.com/fontlabcom/fontlab-fontlabapp/blob/main/examples/native_ui.py)
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

The MCP SDK (v1 or v2 line) owns framing, authentication, process spawning and teardown. A
small relay normalizes only isError:null, preserving actual true error flags and
RPC errors. Its downstream writer channel closes before transport teardown;
otherwise the SDK server writer prevents upstream child cleanup. The dedicated
relay process gives its child 0.25 seconds of EOF grace before SDK termination,
inside its parent's two-second shutdown window. This changes process cleanup
only, not FontLab's Python execution deadline. The constant exists in SDK 1.26,
1.30 and 2.3; the adjustment is isolated to the relay subprocess.

Remopy runs on both MCP SDK lines (`mcp>=1.26,<3`). `mcp/compat.py` holds the only
differences it meets: v2's snake_case fields (`is_error`, `next_cursor`), wire dumps
with `by_alias=True`, and v1's RootModel wrapper around JSON-RPC messages. Test both:

```sh
uv sync --extra test
./test.sh                                                        # locked SDK (2.x)
uv run --extra test --with "mcp==1.30.0" python -m pytest -q     # v1 line
uv run --extra test --with "mcp==1.26.0" python -m pytest -q     # v1 floor
uv build
```

The test suite (run against mcp 2.3.0, 1.30.0 and 1.26.0 at commit 907d014) covers reusable sync/async sessions, decorated functions,
JSON/Unicode/stream transport, source failures, native error parsing, extended preference
setup, normalization, real SDK framing and timeout child-process cleanup by PID.
Envelope regressions cover Unicode separators, missing/duplicate/malformed and
oversized results, and verify that decoding failures never replay operations.
Live checks verify nonce-matched .flpy execution through MCP, launch, native
preference setup and the authenticated tool catalogue in FontLab 9 (46 tools at
migration, 47 in the later MCP v2 session). Installed-artifact
checks and project-wide release gates are recorded in WORK.md.

MIGRATION.json retains historical source hashes and the recovery archive digest.
No recovery archive is present in this checkout or its distributions; this
change does not relicense historical recovery bytes. Current first-party
source and documentation are licensed under [Apache-2.0](LICENSE), with the
Fontlab Ltd. copyright retained in [NOTICE](NOTICE). Third-party materials keep
their original terms and notices. Versions use hatch-vcs and Git tags.

## Package layout

Public imports such as `from fontlab_remopy import FontLab` are unchanged and
remain lazy. `client.py` provides the sync/async clients, `actions.py` their named
controls and `python()` decorator, `remote.py` function transport, `results.py`
execution envelopes, and import-light `host.py` the in-FontLab helper. `setup.py`
uses the `platforms` layer; application launch/submission lives in `platforms/macos/`.
Unsupported launch/submission errors name the platform; explicit bridge discovery
remains available for MCP use outside macOS.

`mcp/` contains transport APIs, `compat.py` isolates SDK version differences, and
`relay.py` runs as `python -m fontlab_remopy.mcp.relay <command>`. The deprecated
`python -m fontlab_remopy.mcp_bridge <command>` entry point and its `normalize_result`
and `relay` imports remain compatible with saved MCP configurations. They now emit a
`DeprecationWarning` on stderr; stdout stays reserved for MCP. Aidus uses the relay.
Remopy 2.0 removed the eight pre-1.2 module paths (`control`, `controls`, `execution`,
`functions`, `launch_api`, `mcp_api`, `mcp_compat`, `native`); the CHANGELOG
lists the replacement import for each.

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

## Status

Issue 101 migration and the added control scope are complete and released as
verified v0.2.0 (RELEASE.md): launch, `.flpy`, MCP setup/catalogue/calls,
synchronous and asynchronous contexts, decorated remote functions, JSON/Unicode
results and streams, errors, per-call deadlines with unknown-outcome fencing and
process cleanup, all checked from installed artifacts in FontLab.

## Issue 233 source/build-only documentation

Maintained site source is `src_docs/md`, configured by `src_docs/mkdocs.yml`;
`docs/` is generated output. Use a separate Python 3.13 docs environment, uv
0.13.7 and the exact hash-locked requirements. Run `sh src_docs/build.sh` and
`python -m unittest discover -s tests_docs -v` with that environment on PATH.
Every main push builds exact source X, optionally makes a normal docs-only child
Y, and independently verifies immutable lineage, source identity, source epoch
and complete tracked/untracked generated parity. No private Pages permission,
configuration, deployment or automatic publication request is enabled.
Source/generated review, actual Actions, owner installation and native acceptance
remain separate. Do not change runtime dependencies, startup or recovery pins for
a site build.
