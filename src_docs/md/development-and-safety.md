---
this_file: src_docs/md/development-and-safety.md
---

# Development and safety

## MCP SDK compatibility

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
Historical installed/native receipts remain separate from the current source and website. Requalify setup, catalogue, nonce-verified script execution and launch on the actual supported host before claiming current native acceptance.


## Execution limits and ownership

The native `run_python` deadline is fixed at five seconds, with 32768-byte code and 65536-byte output bounds. A client wait timeout does not stop native execution; deferred event-loop work outlives the scheduling call. Never replay a mutation after timeout, cancellation or a result decoding failure. Inspect native state before choosing another operation; reopen a fenced session before new calls.

Do not clear native Output, global update queues or owner resources. `fl.output()` reads MCP's recent captured log; App's native output helper reads a different panel. Use owned fixtures and a document-free dedicated session for native mutation. Native UI examples now belong to App, including `examples/native_ui.py`; do not recreate a duplicate in Remopy. They require App installed in the host, retain their native handles across calls, wait outside the UI thread and release only their owned resources. Optional TypeRig composition remains a separate installed dependency and native qualification.

Native PythonQt instances reject new attributes; use `QByteArray.data()` instead of `bytes(QByteArray)`. Disconnect owned signals before `deleteLater()`, and do not disconnect a receiver that holds both native-slot and bound-method handlers. Never close a font while its Save Changes dialog is open. A runaway host call or timeout is not proof that host work stopped. Use the workspace's guarded native runner for authorized native work; the website never invokes it.

## Public imports and compatibility paths

Public `FontLab` and `AsyncFontLab` imports remain lazy. Remopy 2.0 removed the eight pre-1.2 module paths (`control`, `controls`, `execution`, `functions`, `launch_api`, `mcp_api`, `mcp_compat`, `native`); the CHANGELOG lists the replacement for each. The deprecated `python -m fontlab_remopy.mcp_bridge <command>` entry point and its `normalize_result` and `relay` imports remain compatible with saved MCP configurations; they emit a `DeprecationWarning` on stderr and never write to stdout, which carries MCP. The current relay entry point is `python -m fontlab_remopy.mcp.relay <command>`. SDK framing, authentication and spawning remain SDK-owned. Normalization preserves true tool errors and RPC errors; child cleanup timing does not change the native Python deadline.

## Website checks

Use a separate Python 3.13 environment and uv 0.13.7, install `src_docs/requirements.txt` with `--require-hashes`, then run `sh src_docs/build.sh` and `python -m unittest discover -s tests_docs -v`. The build uses the source commit's timestamp once for deterministic output. Every main push builds the exact source SHA, publishes a normal docs-only child only when output changes, then verifies the immutable source/output lineage and independently rebuilds all output. Private Pages permissions and requests remain disabled.

Source, ordinary installed origins, all three SDK suites, native behavior, canonical adoption and publication are distinct gates. Issue 123 remains paused. The website does not establish a fresh SDK or native result.
