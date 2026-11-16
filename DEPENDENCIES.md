---
this_file: DEPENDENCIES.md
---

## Conditional installer requirements

Only conditional installer requirements use `packaging==26.3` in an external uv-managed Python environment. FontLab itself imports only the standard library; no permanent project dependency was added. An unavailable helper fails before sibling execution.


# Dependencies

The synchronous control API reuses the AnyIO blocking portal and the MCP SDK; it
adds no runtime package. The transport lives in `fontlab_remopy.mcp`; absolute
`mcp` imports still refer to the SDK. macOS launch code lives in `platforms/macos/`.
Ordinary remote functions use Python's inspect, AST and signature binding rather
than a proxy or serialization framework.

- `mcp>=1.26,<3` (MIT): official MCP SDK; framing, typed messages, stdio lifecycle.
  Both lines are supported (migration 2026-10-15): `mcp/compat.py` bridges v2's
  snake_case fields and v1's RootModel message wrapper. The full suite passes on
  1.26.0, 1.30.0 and 2.3.0, and a read-only native session against FontLab's
  `fontlab-mcp` bridge passes on 1.30.0 and 2.3.0. A consumer that pins `mcp<2`
  (fontlab-aidus-agentus's brain) still resolves to v1. v2 adds opentelemetry-api,
  httpx2 and mcp-types (and drops httpx/httpx-sse); cryptography and PyJWT were
  already transitive dependencies on v1 (1.26), and v2 imports cryptography when
  `mcp` is imported. If remopy goes into FontLab's host-packages, every compiled
  wheel must be arm64 Python 3.11 (verified: `import mcp` 2.3.0 on arm64 CPython
  3.11; an x86_64 interpreter produced an unloadable cryptography binding).
- `anyio>=4.12,<5` (MIT): structured relay concurrency and stream closure
  (verified 4.12.1, 4.15.1).
- Standard library subprocess, pathlib, json, asyncio, tempfile, inspect, ast:
  launch, verified setup, remote-function binding.
- `glyphs/fontlab_remote.py` (the Glyphs.app script) uses only the standard
  library and GlyphsApp.
- hatchling and hatch-vcs: wheel/sdist and Git-tag versions. pytest and
  pytest-asyncio: tests, including real subprocesses.

Inside FontLab, `fontlab` is imported lazily from the host. If remopy is installed
into FontLab's host-packages, the environment must be arm64 Python 3.11: mcp
brings compiled wheels (pydantic-core and others).

Re-evaluated 2026-10-15 (R046).

Official SDK docs/source consulted:
[v1.26 README](https://github.com/modelcontextprotocol/python-sdk/blob/v1.26.0/README.md),
[v1.30 stdio](https://github.com/modelcontextprotocol/python-sdk/blob/v1.30.0/src/mcp/client/stdio/__init__.py),
[v1.30 ClientSession](https://github.com/modelcontextprotocol/python-sdk/blob/v1.30.0/src/mcp/client/session.py).
Development environment: mcp 2.3.0 / anyio 4.15.1; the suite also runs on mcp 1.30.0
and 1.26.0 (README). The process-local SDK cleanup constant exists in 1.26, 1.30
and 2.3. v2 migration guide: https://py.sdk.modelcontextprotocol.io/v2/migration/

## Independent documentation environment

Python 3.13 and uv 0.13.7 build the site separately from the product runtime.
`src_docs/requirements.txt` retains all 31 exact hash-locked dependencies from
the qualified ProperDocs pipeline: ProperDocs 1.6.7, MkDocs 1.6.1, MaterialX
10.1.8 and PyMdown Extensions 11.0.1. Runtime dependencies and locks are unchanged.
The fltheme26 1.0.0 light components and FontLab menu load as frontend assets;
the generated MaterialX assets retain their own vendor licence notices.
