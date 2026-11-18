---
this_file: TODO.md
---

- [ ] Issue 271: independently review and integrate the generated installer through repository gates, verify exact-SHA CI/archives, and qualify macOS/Windows native execution after serialized admission.



# Next steps (functional first)

1. Reconcile launch/catalogue/command changes with App and Aidus consumers and supported MCP SDK paths (source, focused checks).
2. Deliver the guarded common installer candidate (Instamix 1.0.11 stub): review, fresh-main reconciliation, hook, exact-SHA CI, release.
3. Requalify installed launch/catalogue/nonce execution and App `native_ui.py` in FontLab. Blocked: the 9.1.9813 `fontlab-mcp` bridge SIGSEGV (track fl#8657); until fixed, run probes as `.vfpy` writing results to a file.
4. Windows/CrossOver submission review (Issue 256).
5. Parked, owner-held or process-only rows are at the end.

## Guarded common installer (also covers the 2026-11-15 shared-installer candidate)

- [ ] Obtain independent final review, current graph qualification and fresh-main reconciliation of the canonical 1.0.11 template and preserved metadata/archive/licence contracts.
- [ ] Qualify the ordinary push hook, exact-commit CI and genuine release/archive/download inputs on the final source; repeat the three-SDK checks if its source or dependency tuple changes.
- [ ] After admission, qualify the full installed provider/consumer cohort, owner recovery and native/Windows receipts; retain Aidus/Fly, unknown Windows replay and private Pages holds.
- [ ] Obtain independent merge review and fresh-main reconciliation, then deliver the candidate through the hooks and combined-source gates, exact-SHA CI and a genuine tag/release/download qualification (merged from the 2026-11-15 shared-installer rows).

## Functional and native

- [ ] Reconcile launch/catalogue/command changes with App and Aidus consumers and supported MCP SDK paths using focused checks before the detailed installed-host pass; never replay an unknown mutation.
- [ ] After qualified main integration, inventory obsolete branches/files, preserve unique work and remove only proven stale items with recovery evidence.
- [ ] Requalify installed launch/catalogue/nonce execution (setup, catalogue, `.flpy` nonce execution, launch) on the supported host, and run [App's `examples/native_ui.py`](https://github.com/fontlabcom/fontlab-fontlabapp/blob/main/examples/native_ui.py) in FontLab against the current App/Remopy (panel, dialog, Preview drawing, removal). Blocked: the 9.1.9813 `fontlab-mcp` bridge crashes with SIGSEGV in `BridgeConnection::updateTimeout`, so `run`/`tools`/`setup` time out; track [fontlab/fl#8657](https://github.com/Fontlab/fl/issues/8657). The source half is tested: `tests/test_consumer_imports.py`. Timeouts do not cancel host code.
- [ ] After owner access restoration, audit actual process/build/documents/dirty state/fences before native qualification.
- [ ] Run the exact repository checks on the integrated source, obtain independent review, commit/push the scoped milestone and verify its remote head.

## Issue 256 Windows submission — 2026-11-17

- [ ] Obtain independent review and fresh-main delivery qualification for the CrossOver/Wine launch and submit candidate.
- [ ] After native admission, verify actual CrossOver/Wine receipt-backed script execution without replaying unknown outcomes.
- [ ] Qualify Windows standalone Python/uv bootstrap, owned wheel installation, embedded imports and native MCP discovery separately.

## Later, owner-held or parked

- [ ] Remove the deprecated `fontlab_remopy.mcp_bridge` entry point in the major release after 2.0 (owner Q6=A: it stays one major longer because saved MCP configs may run it). Replace `tests/test_mcp_bridge_deprecation.py` with a `ModuleNotFoundError` test, update `MIGRATION.json` and README, and have python-docs regenerate its pages.
- [ ] Independent review of the Remopy Issue 233 site pages and content. The source contract, the no-Pages-grant workflow and the exact-SHA Documentation runs were verified read-only on 2026-11-11 (run 43103213565 and earlier; see the Issue 250 triage audit remopy-row17-audit.md). The browser and light-mode check stays blocked while private Pages is owner-held. Bot-child pushes use `GITHUB_TOKEN` and trigger no run by design.
- [ ] Resolve the original archive contract without treating the 2.0.2 Apache source/release/download/prefix checks as archive acceptance. Preserve external recovery, the historical 149-file raw-mode FAIL and frozen MIGRATION.json hashes; private Pages remains held. Actual FontLab installation/native checks remain open above.
