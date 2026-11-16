---
this_file: TODO.md
---

## Shared installer qualification — 2026-11-15

- [ ] Deliver the source-reviewed, three-SDK-qualified shared-installer candidate through fresh-main reconciliation, independent merge review, normal hooks/combined-source gates, main delivery/exact-SHA CI and genuine tag/release/download qualification.
- [ ] After admission, verify installed provider/consumer identity and the applicable Script/Extension/native workflows without clearing existing holds by inference.



# Open tasks

- [ ] Remove the deprecated `fontlab_remopy.mcp_bridge` entry point in the major release after 2.0 (owner Q6=A: it stays one major longer because saved MCP configs may run it). Replace `tests/test_mcp_bridge_deprecation.py` with a `ModuleNotFoundError` test, update `MIGRATION.json` and README, and have python-docs regenerate its pages.
- [ ] Requalify installed launch/catalogue/nonce execution on the supported host and the App-owned native UI consumer; timeouts do not cancel host code.
- [ ] Run the exact repository checks on the integrated source, obtain independent review, commit/push the scoped milestone and verify its remote head.
- [ ] After qualified main integration, inventory obsolete branches/files, preserve unique work and remove only proven stale items with recovery evidence.

- [ ] Re-run installed-artifact native checks (setup, catalogue, `.flpy` nonce execution, launch) on the current FontLab build.
- [ ] Run [App's `examples/native_ui.py`](https://github.com/fontlabcom/fontlab-fontlabapp/blob/main/examples/native_ui.py) in FontLab against the current App/Remopy (panel, dialog, Preview drawing, removal). The source half is tested: `tests/test_consumer_imports.py`.

- [ ] After owner access restoration, audit actual process/build/documents/dirty state/fences before native qualification.

- [ ] Independent review of the Remopy Issue 233 site pages and content. The source contract, the no-Pages-grant workflow and the exact-SHA Documentation runs were verified read-only on 2026-11-11 (run 43103213565 and earlier; see the Issue 250 triage audit remopy-row17-audit.md). The browser and light-mode check stays blocked while private Pages is owner-held. Bot-child pushes use `GITHUB_TOKEN` and trigger no run by design.
- [ ] Resolve the original archive contract without treating the 2.0.2 Apache source/release/download/prefix checks as archive acceptance. Preserve external recovery, the historical 149-file raw-mode FAIL and frozen MIGRATION.json hashes; private Pages remains held. Actual FontLab installation/native checks remain open above.
