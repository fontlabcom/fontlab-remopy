---
this_file: src_docs/md/installation.md
---

# Installation

Use Python 3.11 or newer for Remopy. FontLab's host environment is arm64 Python 3.11; an x86_64 interpreter cannot be loaded into that host. External clients and the website build use separate environments.

From an authorized source checkout, install into an external Python environment:

```sh
uv venv --python 3.11
uv pip install --python .venv/bin/python .
```

The runtime dependencies remain `mcp>=1.26,<3` and `anyio`. Native application launch and file submission support macOS and Windows. On Windows the default application is `%ProgramFiles%\Fontlab\FontLab 9\FontLab 9.exe`; Python callers may pass a full executable path as `app`. Discovery checks an explicit bridge argument or `FONTLAB_MCP_COMMAND`, then PATH or the installed FontLab 9 application. The legacy `AIDUS_FONTLAB_MCP_COMMAND` remains accepted. A missing explicit executable never silently chooses a different FontLab build.

For Glyphs 3/4, use the separate [standard-library script](api-and-glyphs-cli.md#remote-control-fontlab-from-glyphs): its Python needs no Remopy installation. Python 3.8+ is the stated minimum; retained runs used Python 3.9 and 3.13. Configure Glyphs' Python framework before using its Scripts menu.

Inside FontLab, enabling MCP updates only the extended preference and notifies the host; it does not save all preferences or clear logs. Owner-managed installation, native preference changes and running a script require their own acceptance. This documentation build performs none of them.
