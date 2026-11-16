---
this_file: src_docs/md/index.md
---

# Remopy for FontLab

Control FontLab from external Python through its authenticated native MCP bridge, or from Glyphs through a standard-library client. Remopy supplies reusable synchronous and asynchronous sessions, JSON function transport, launch and script submission. It does not depend on AI libraries or agent prompts.

Start with [installation](installation.md), then the complete [API, CLI and Glyphs reference](api-and-glyphs-cli.md). Read [development and safety](development-and-safety.md) before calling a mutating tool. See the [proprietary licence](licence.md).

A client timeout leaves the execution outcome unknown. It does not cancel FontLab code, and timed-out mutations must never be retried automatically. Ordinary source tests, installed artifacts and native host acceptance are separate results.

The website is built from maintained Markdown without importing the product, starting clients or servers, or contacting FontLab. Its configured site URL is a future repository identity; private Pages publication remains owner-held.
