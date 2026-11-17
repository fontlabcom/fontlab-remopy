---
this_file: CHANGELOG.md
---

## 2.0.4 (2026-11-16)

- `install.vfpy` is now the short fontlab-instamix stub. It installs
  fontlab-instamix from PyPI when it is missing, then installs this checkout from
  its `[tool.fontlab-install]` table. The large legacy installer is gone.
- `tests/test_installer_archive.py` tests the stub, the install table and the sdist.
- README describes the stub install.

## 2026-11-15 — Shared installer source alignment

Copied the reviewed shared installer exactly: dependency constraints and managed origins remain protected; inactive conditional dependencies are filtered before sibling execution in the resolver target Python. FontLab imports remain standard-library-only. Package identity, runtime APIs, dependency declarations, scripts, bundles and legal files are unchanged. The real source-archive check now includes the exact root installer; the prior omission was reproduced before the single allowlist addition.

Fresh isolated successor: the eight reviewed source postimages were hash-verified before transfer; the approved AGENTS priority amendment is separate. Independent source review passed. Focused archive/layout checks pass on Python 3.11 arm64 (9 passed). Controller full-suite checks passed on locked SDK, MCP 1.30.0 and MCP 1.26.0: each 179 passed with one existing missing-App-sibling skip, in 21.66/26.07/26.61 seconds pytest time (22.05/26.78/27.03 seconds command elapsed). The lock remains byte-exact. The older attempt remains held; historical graph scope and control-state uncertainty remain open. Normal hooks, fresh-main merge and independent merge review, main delivery/CI, tag/release/downloads, installed provider closure and admitted FontLab/native/full-cohort workflows remain pending. No owner-folder installation or native operation ran.



## 2026-11-14 — Remopy 2.0.2 Apache release qualified

[Remopy v2.0.2](https://github.com/fontlabcom/fontlab-remopy/releases/tag/v2.0.2) binds source/main `00d200b8924e5663e513f6f545882ec9bb4ef27a`; annotated tag object `5ce9244f53300a0ccddac6a64c4de28faa1a66fd` peels to that source. The unchanged ordinary main hook passed 179 tests without skips in 31.06s, with all 16 production modules at least 80% combined coverage; the ordinary tag hook passed 179 tests in 30.55s. Exact-source CI43646468359 passed both 37-test documentation jobs with SOURCE==OUTPUT==that commit.

The two published assets were actually downloaded. Wheel SHA-256 `b320677b15eea41f53eec38393a1a9631a2ae728f18056c0c572d7fb7dcc16e8`; sdist SHA-256 `26205280fd20cb3513d565e3eb75c41b30626621eec535d582cdf43b37057030`. Current first-party source/docs and legal metadata use owner-authorized Apache-2.0; 47 inserted headers preserve runtime ASTs, third-party bytes/notices and frozen MIGRATION.json. All 17 runtime files and installed RECORD validate in a fresh prefix from the downloaded wheel; 78 transport/SDK/API tests passed in 11.05s with one warning and no native providers. Earlier three-SDK runs retain 178 passes and the missing-App-sibling skip; a real-App focused check passed six tests, and the final hook passed without that skip.

Independent postpublication REMOPY-RELEASE-REVIEW.md approves these bounded source/release/download/prefix results. The original archive contract and T17 remain open; the historical 149-file raw-mode FAIL is retained. Root install.sh, FontLab installation/native behavior, history/save-reopen, private Pages and cleanup were not performed.

## 2026-11-14 — Apache-2.0 source qualification

- Apply owner-authorized Apache-2.0 to current first-party source and documentation;
  retain the 2025 Fontlab Ltd. copyright in NOTICE, include both legal files in
  wheel/sdist, and add SPDX headers to 47 authored Python/shell/vfpy files.
- Correct stale in-repository recovery claims without changing MIGRATION.json;
  preserve all third-party frontend assets, source maps and notices byte-for-byte.
- Verify actual wheel/sdist legal bytes and metadata, all three SDK contexts
  (178 passed, one existing App-sibling skip and one warning each), strict docs
  and 37 documentation tests. Runtime code bodies and tracked modes are unchanged.
- Source candidate only: independent review, integration, released artifacts,
  installation and native acceptance remain separate; private Pages stays held.

## 2026-11-14 — Guarded documentation repair delivered to main

- Independent review approved the exact five-file source change
  [aab6906](https://github.com/fontlabcom/fontlab-remopy/commit/aab6906aba43404eccbb584b39b0d1a4d27506ad)
  (tree `32a4b2f29156728cf61480e86af949286c15f78c`). All 149 tracked
  payloads and raw modes were verified; 144 unrelated files were unchanged.
- The unchanged installed pre-push hook passed 178 tests with one existing
  warning in 28.18 seconds through the ordinary push (33.89 seconds). It
  identified zero changed production modules; this is not a coverage result.
  An earlier detached-checkout push failed before tests. A new owned tracking
  branch at the same commit/tree supplied the real upstream baseline; no
  owner branch changed and no hook was bypassed.
- [Documentation run 43581035677](https://github.com/fontlabcom/fontlab-remopy/actions/runs/43581035677)
  passed both jobs on attempt 1. Its generated-only child
  [58f30ba](https://github.com/fontlabcom/fontlab-remopy/commit/58f30ba1fde71e11389c37044f36a336ea0f1760)
  has sole parent aab6906 and changes only the two sitemap files. Qualification
  verified all 48 generated payloads and source epoch 1794648574. Four
  controller phases verified the captured owner files, admin, indexes, refs
  and attachments. Archive modes and checkout raw modes remain separate.
- Closed only this repair's review/main/hook/CI follow-up. Six inherited
  expanded Ruff 0.14.10 findings, limited graph coverage and historical index
  uncertainty remain. Release, artifacts, providers, licence migration, root
  installer completion, all native/GUI/theme/typing/history checks, private
  Pages and cleanup holds remain open. This entry records the delivered
  repair; delivery of this progress update is not yet claimed.

## 2026-11-14 — Guarded documentation comparison, isolated source verification

- Replaced the docs test's filename-only observation with a shared content/mode
  patch at the same WORKTREE-to-INDEX boundary. External diff and text conversion
  are disabled; every original output hash/count, source epoch and lineage
  assertion remains. The added real Git five-state regression preserves index
  bytes/mode and rejects content, deletion and executable-mode changes.
- Reproduced the original failure and both regression false positives before
  repair. All 37 docs cases then pass; the strict hash-locked build reproduces
  all 48 output payloads and raw modes. Each advertised SDK context passes the
  same 178 runtime cases. A genuine App v1.2.16 source peer changes the existing
  AST/signature skip to a pass. No native App or FontLab behavior is inferred.
- Complete-package combined coverage is 95.49%; all 16 modules exceed 80%
  (minimum 84.06%). Selected Ruff 0.14.10 passes production and the changed
  test, while its expanded scope still reports six existing test_remote.py
  findings. Explicit Ruff 0.16.7 passes the expanded scope.
- Archived the complete previous WORK.md privately before updating progress.
  Independent review, combined delivery checks, main/hook/exact-commit CI,
  release, owner installation, native acceptance and licence migration remain
  open. This entry records isolated verification only.

## 2026-11-14 — Functional work order documented

- Added the owner's functional-progress-first guidance and repository-specific priorities, including cross-package compatibility and a later detailed testing pass. Existing mandatory hooks, holds and unfinished work remain in force.
- This change updates guidance and planning only; it establishes no new runtime, installed, native or release result.

## 2026-11-12 — D46 documentation pass (Issue 250)

- Landed on `main` this session: `1f29bfa` (Ruff lint debt cleared, 44 findings to zero), `ff3b992` (test environment qualification), `297253d` (legacy `mcp_bridge` entry point warns on stderr only), `4c7782b` (2.0.0: eight deprecated pre-1.2 modules removed), `81b67ca` and `44dada7` (R7a Aidus relay migration closed; Issue 207 distribution comparison closed, shim-removal decision row opened). No source changed in this pass.
- New open TODO row: the Q5 licence audit (D46 licence rows).
- `WORK.md` now holds a short current status. Its previous 2,210-byte content (SHA-256 `8e2b1df16b76dd006c2cbf44a4e009b1cf0e0ce6b8e6561938f8c16dd67a5b68`, the Issue 250 lint-only round: Ruff 0.16.7, 151 passed on three MCP SDK lines, docs suite 36 tests with 2 failures and 11 errors both before and after) is archived on the workspace data volume.

## 2026-11-12 — Breaking (2.0.0): eight deprecated modules removed (Issue 250)

- The owner chose removal (Q6=A). The eight pre-1.2 warning shims are gone; importing them raises `ModuleNotFoundError`. Change imports as follows:

| Removed import | Use instead |
| --- | --- |
| `fontlab_remopy.control` | `fontlab_remopy.client` (`FontLab`, `AsyncFontLab`) |
| `fontlab_remopy.controls` | `fontlab_remopy.actions` (`Controls`) |
| `fontlab_remopy.functions` | `fontlab_remopy.remote` (`remote_function`) |
| `fontlab_remopy.execution` | `fontlab_remopy.results` (`ExecutionResult`, `ResultTransportError`, `encode_execution`, `decode_execution`, `MAX_CODE_BYTES`, `MAX_OUTPUT_BYTES`) |
| `fontlab_remopy.native` | `fontlab_remopy.host` (`enable_mcp`) |
| `fontlab_remopy.mcp_api` | `fontlab_remopy.mcp` (`NativeExecutionError`, `bridge_parameters`, `probe_tools`, `call_tool`, `run_python`, `execute_script`) |
| `fontlab_remopy.mcp_compat` | `fontlab_remopy.mcp.compat` (`field`, `is_error`, `next_cursor`, `wire`, `unwrap`) |
| `fontlab_remopy.launch_api` | `fontlab_remopy.platforms` (`ScriptSubmission`, `find_bridge`, `launch`, `submit_script`, `DEFAULT_APP`) |

- `fontlab_remopy.mcp_bridge` still ships with its stderr `DeprecationWarning` and goes one major later.
- `tests/test_deprecated_modules.py` now checks that each removed path raises `ModuleNotFoundError`, is absent from the package, and that its replacement module provides every moved name; it also checks that `mcp_bridge` still ships.
- A caller re-audit of current remote mains (Aidus, App, Scriptmix, Plugmix, Examples, python-docs, Glyport, Fontport) found no code importer. The only hits are `tools/migrate_app_paths.py` rewrite tables, which keep the old names as inputs, and python-docs generated pages, which python-docs regenerates after the 2.0.0 release.

## 2026-11-12 — `mcp_bridge` deprecation warning (Issue 250)

- `fontlab_remopy.mcp_bridge` now emits `DeprecationWarning` naming `fontlab_remopy.mcp.relay`, like the other eight shims. Under `python -m` the warning is attributed to `__main__`, so the default filters print it on stderr.
- Stdout stays byte-clean: it carries the MCP stdio protocol. New tests in `tests/test_mcp_bridge_deprecation.py` pin the import warning, the stderr warning under default filters and empty stdout; the real SDK round trip through `mcp_bridge` in `tests/test_sdk.py` still passes.
- The module comment and README no longer say Aidus imports it; Aidus writes `-m fontlab_remopy.mcp.relay`.
- Nothing is removed. Removing the shims needs a major release and an owner decision (caller audit: no maintained repository imports them).

## 2026-11-12 — Issue 207 distribution comparison closed (Issue 250)

- The comparison half of the TODO row "Issue 207 distribution changes" is closed: it cannot be done, and no action was owed.
  - The isolated Issue 207 Remopy candidate (`issue-207` successor, base 9957af31) no longer exists; it was an uncommitted tree and has been cleaned up.
  - No Remopy distribution manifest was recorded for it. The only surviving record is the preflight status list in `verification/issue-207/canonical-delivery-preflight.json` (workspace root): it shows the candidate deleted nine modules and edited docs and four tests.
- The nine modules (`control`, `controls`, `execution`, `functions`, `launch_api`, `mcp_api`, `mcp_bridge`, `mcp_compat`, `native`) remain on main as deliberate deprecation shims, so the supported import paths stay.
- Whether to remove them is now its own open TODO row, pending a caller audit.

## 2026-11-12 — Aidus relay migration (R7a) closed (Issue 250)

- The R7a half of the TODO row "Migrate the Aidus generator and guides from `fontlab_remopy.mcp_bridge` to `fontlab_remopy.mcp.relay`" is closed. It was already done in Aidus `main` 3ed19d7 (v1.1.10), the evidence for which follows:
  - The generator launches `-m fontlab_remopy.mcp.relay` (`src/fontlab_aidus_agentus/core/fontlab_mcp.py:138`).
  - The guides name only the relay (`src_docs/md/guides/external-agents-mcp.md:101,110,115`, `src_docs/md/guides/fontlab-mcp.md:67`).
  - `git grep mcp_bridge` outside CHANGELOG finds only a pytest fixture named `mcp_bridge` in `tests/core/test_mcp_roundtrip.py`, not an import.
  - Aidus tests already pin the generator: `test_server_config_when_generated_then_launches_the_mcp_relay_module` and `test_server_config_when_relay_module_named_then_it_is_importable` (`tests/core/test_mcp_roundtrip.py:191-202`).
- The eight deprecated shims and `mcp_bridge` stay for saved user configs, as `tests/test_deprecated_modules.py` pins. The Issue 207 distribution check stays open as its own row. No code change.

## 2026-11-11 — consumer imports and App native_ui source re-check pinned (Issue 250)

- New `tests/test_consumer_imports.py`. `FontLab`, `enable_mcp`, `find_bridge`, `probe_tools` and `bridge_parameters` (the top-level names other maintained repositories import) must stay in `_EXPORTS` and `__all__` and resolve lazily to their canonical objects. App's `examples/native_ui.py` (App 7f96170) is parsed from the sibling checkout: it imports only `FontLab` from `fontlab_remopy`, calls it with no arguments as a context manager, and decorates helpers with `fl.python`; the test checks those names and the `python(self, function)` signature.
- The eight deprecated shims were already pinned by `tests/test_deprecated_modules.py` (identical module and named objects, `DeprecationWarning` naming the replacement) and the `mcp_bridge` relay entry point by `tests/test_sdk.py:31`; no duplicate test was added.
- Mutants: dropping `find_bridge` from `_EXPORTS` fails 1 consumer test; making `python`'s `function` keyword-only (`def python(self, *, function)`) or adding a required keyword argument each fail the native_ui test; silencing the `native` shim's warning fails 1 deprecation test; replacing the `control` alias with a subclass copy fails 1 deprecation test.
- TODO: row 7 now names the Aidus relay migration (R7a) and keeps the Issue 207 check (nothing pending visible on origin/main; compare the isolated candidate's manifest); the native_ui row keeps only the native run.

## 2026-11-10 — three MCP SDK lines re-run from the isolated successor (Issue 250)

On origin/main 262dbac, `uv run --extra test python -m pytest -q` passed 152
tests on each of the locked SDK 2.x line, `mcp==1.30.0` and `mcp==1.26.0`
(arm64 Python from uv, no failures or skips). Offline SDK fixtures only; native
proof stays separate.

## 2026-11-11 — Issue 250 documentation environment

- Document the separate locked Python 3.13 docs recipe. With the clean hash-locked install (`mkdocs-materialx==10.1.8`), all 36 docs tests pass; MaterialX 10.2 reproduces the earlier errors. SDK suite via the workspace recipe: 152 passed (the push gate also ran the added `__main__` entry test). No source or test change.


## 2026-11-10 — live font editing rule (Issue 250, D44)

- AGENTS.md: agents test and edit the font open in FontLab 9, starting from the Desktop VFJs, and may save them.

## 2026-11-10 — Issue 250 Ruff lint cleanup

- Add `test_package_entry_when_run_as_module_then_exits_with_cli_status` so the touched `__main__.py` meets the 80% changed-module coverage gate.
- Merge the nested `async with` in `src/fontlab_remopy/mcp/__init__.py` (SIM117) into one parenthesized statement so Ruff 0.17.4 also reports 0 (checked with `uvx ruff@0.17.4 check .`; 0.16.7 also 0).
- Clear all 44 Ruff 0.16.7 findings (44 → 0), using safe autofixes and
  reviewed f-string conversions, preserving public names, export order and
  exception behavior. Fourteen formatting expressions match their original
  output in 112 comparisons, including Decimal and Fraction timeout values.
- Keep explained line-level exceptions for session-owned temporary-file
  lifetime (SIM115), CLI error reporting (BLE001), the public malformed-response
  RuntimeError (TRY004), compatibility export order (RUF022), and the ProperDocs
  import's initialization side effects (F401). Retain the existing B017 fixture
  exception; remove its unused PT011 suppression.
- Runtime suite: 151 passed before and after (152 at the push gate, which includes the added `__main__` entry test) on each of MCP 2.3.0, 1.30.0 and
  1.26.0. Run existing Python 3.13 with source/cached SDK paths and explicit
  pytest-asyncio, without installation; see WORK.md for the command.
- Additional documentation suite: 36 tests before and after, with the same
  2 failures and 11 errors from the existing documentation environment and
  asset mismatch. No new failures. Ruff ran from the installed uv tool because
  uvx could not acquire its sandbox-protected cache lock.
- No Ruff configuration or whole-file formatting changes; legacy/frozen
  evidence, native FontLab, installation and publication remain untouched.

## 2026-11-10 — isolated graph guidance proposal

Prepare append-only AGENTS guidance for separate task-owned graph HOME and storage, ordinary-analysis scope and independently reviewed bounded recovery. Preserve existing integration rules and acceptance holds. This documentation proposal records no new runtime, test, native, integration or publication result.

## 2026-11-10 — verified integration-round guidance

- Record current-main reconciliation in a new isolated successor, preservation
  of concurrent work and exact reviewed staging, combined repository/graph
  checks, independent merge review, required hooks and actual remote proof.
- Keep solved tasks in cumulative history and unfinished acceptance in the
  future queue. Native, installation, adoption, Issue 123 and private Pages
  boundaries remain unchanged. This entry records documentation only.

## 2026-11-10 — install.vfpy always reinstalls scripts and dependencies

- Every install copies all files from `Scripts/` afresh and replaces any file
  already at the same path. A symlinked script folder is replaced by a real
  folder; the link target is never written. A directory where a script file
  belongs is still refused.
- Required packages are installed on every run. Packages that no package
  index carries (the fontlab-* packages, pythonqtside) are installed from
  checkouts beside this one through their own `install.vfpy`, once per run
  and safe against cycles. uv receives every other requirement, so version
  ranges, markers and extras are enforced. Without uv, sibling checkouts are
  still installed and only the remaining missing requirements are reported.
- The installer is byte-identical across all eleven installer repositories.

## 2026-11-05 — independently approved documentation applied

[Task 2 final review](../verification/issue-230/task-2-fix2-review.md) records
SPEC PASS / QUALITY APPROVED. The [78-file application receipt](../verification/issue-230/task-2-apply.json)
includes this repository's six guides and preserves all 21 repository heads,
branches, indexes and non-selected diffs. This is applied documentation evidence,
not a new product test, installed artifact, native result or publication.

The complete earlier handoff/history below retains its proposal-stage statements
and dated source pins. Later review, application and delivery status belong in the
[live workspace ledger](../verification/issue-230/progress.md). Original future,
native, artifact and preservation contracts remain binding.

## 2026-11-05 — documentation reconciliation proposal

Prepared repository-specific organization, test and MVP/delivery guidance from current source/test configuration and retained Issue 207–211 evidence. Distinguished current canonical layout from qualified candidates, future plugin ownership and unfinished native/artifact gates. Preserved all prior work and changelog evidence; no runtime completion, installation or publication is claimed. Historical checked tasks now require receipt/current-scope reconciliation rather than being silently counted complete.

## 2026-11-05 — planning chronology reconciliation

Issue122worktree-only execution and old source-head handoff are superseded. Keep all three SDK lines, installed native/nonce/launch and relocated App UI consumer requirements on the current isolated tuple. Historical passing results retain their dated source and acceptance scope in the entries above and original history below. This documentation change creates no new runtime acceptance.

---
this_file: CHANGELOG.md
---

## 2.0.4 (2026-11-16)

- Move the native UI example to fontlab-fontlabapp; retain a guide link and
  current native requalification task instead of a duplicate implementation.
- Merge the Issue 201/204 branch into the issue 205 layout: the unknown-argument
  guard (`tool_schema`, `unknown_arguments`, `refuse_unknown`) lives in
  `mcp.compat`; `client.AsyncFontLab.tool` and `mcp.call_tool` use it; method
  docstrings live in `client` and `actions`. The deprecated `control`,
  `controls`, `mcp_api` and `mcp_compat` forwarders expose the same objects.

## 1.2.0 — 2026-11-03 — issue 205 package layout

- Rename `control` to `client`, `controls` to `actions`, `functions` to
  `remote`, `execution` to `results`, and `native` to `host`.
- Rename `mcp_api` to `mcp`, `mcp_compat` to `mcp.compat`, and `launch_api`
  to the platform dispatcher `platforms` (macOS implementation in `platforms.macos`).
- Retain all eight old module paths as deprecated forwarders: imports emit
  `DeprecationWarning` and alias the canonical modules, preserving object identity.
- Keep portable bridge discovery and submission data in `discovery`; importing
  `platforms` on other systems no longer imports `platforms.macos`. Unsupported
  launch/submission still raise `NotImplementedError` naming the platform.

- Move clients, named actions, remote functions, result transport and host setup
  into `client.py`, `actions.py`, `remote.py`, `results.py` and `host.py`.
- Group MCP APIs, relay and SDK compatibility under `mcp/`; move macOS launch
  and script submission to `platforms/macos/`, selected through `platforms`.
- Preserve all lazy public exports and the deprecated `mcp_bridge` entry point
  and `normalize_result`/`relay` imports for external configurations and Aidus.
- Update tests, examples and current module references. Dependencies, native
  execution limits, nonce handling and call serialization remain unchanged.

## 2026-11-03 — installer options, licence and cleanup

- `install.vfpy` reads optional `[tool.fontlab-install]` keys: `name` (the distribution
  record), `packages` (`[]` installs scripts only) and `dependencies` (what FontLab needs,
  instead of `project.dependencies`). Symlinks inside `Scripts/` are not copied.

## 2026-11-03 — install.vfpy fixes from runs inside FontLab 9

Verified by installing all nine packages inside FontLab 9 (Python 3.11.6, arm64).
- Dependencies with console scripts (glyphsLib, fontTools) failed: uv writes them to
  `site-packages/../../../bin`, which resolves through the venv link to the FontLab
  folder. `bin`, `share` and `include` there now link back into `.venv`.
- A failed install appends a `"failed"` record with the traceback and uv's output to
  `install.log`; List/Uninstall ignore failed records.
- Package records include `WHEEL`, so `uv pip check` accepts them.
- Scripts are copied file by file into FontLab's `Scripts` folder, from a package's
  `Scripts/` folder (exact case) and from folders listed in `[tool.fontlab-install] scripts`.
  Folders shared by several packages merge, e.g. two packages' `Scripts/Kerning`. The
  installer refuses to overwrite a file another package or the user put there; uninstall
  removes only its own files, their `.pyc`, and folders left empty. An older install's
  folder link (`Scripts/Aidus Code`) is replaced by copied files.
- `*.vfpyc` (FontLab's compiled `install.vfpy`) is ignored by Git.

## 2026-11-03 — install.vfpy creates FontLab's venv

FontLab's `python/3.11/site-packages` is now always a real folder; packages are
symlinked into it, so no `.pth` processing is needed. `install.vfpy` creates `.venv` with
uv from FontLab's exact Python version and processor type, and links the venv's
site-packages to FontLab's folder, so `uv pip install --python .venv/bin/python` installs
into FontLab. An older layout (FontLab's folder linked into `.venv`) is migrated.

## 2026-11-03 — reverse-domain extension id and install.log

`[tool.fontlab-install] id = "com.fontlab.remopy"` names this extension. `install.vfpy` keeps
`Extensions/com.fontlab.remopy/install.log` (JSON Lines; the last line lists every installed file),
puts copied code in `Extensions/com.fontlab.remopy/lib/`, and adds Scripts > Extensions >
List Extensions and Uninstall com.fontlab.remopy.

## 2026-11-03 — install.vfpy without uv

`install.vfpy` now needs only FontLab's Python. It asks FontLab for its data folder
(`flPreferences().dataPathDefault`), links a Git checkout or copies a plain folder into
`Extensions/`, and writes a `.pth` plus `.dist-info` into `python/3.11/site-packages`.
uv is used only to add missing dependencies. It never replaces folders it does not own.

## 2026-11-03 — release scripts

Added `build.sh` (uv build into dist/), `publish.sh` (`uv publish`; refuses a dirty
tree or an untagged HEAD) and `install.vfpy` (editable install into FontLab's venv
from inside FontLab). Version stays hatch-vcs from `vX.Y.Z` tags.

<!-- workspace-handoff:2026-11-03 -->
## 2026-11-03 — documentation handoff for November 2–3

No new November 2–3 runtime delivery is attributed here; the current native-access hold is external to source tests.

No native retry, process restart or fence clearance was performed by this documentation task.

Observed canonical checkout: `main` at `d0afe25a6182`. No source integration is performed by this update.

Updated the requested AGENTS/TODO/PLAN/CHANGELOG/README documentation and
recorded the paused state. Existing project text, examples and history remain;
no runtime source, installation, native session, branch/ref, release or site was
changed by this documentation maintenance. Source/archive/ordinary/native and
promotion acceptance remain separate claims. Detailed workspace evidence is
recorded in the root CHANGELOG and retained verification reports.
<!-- /workspace-handoff -->

# Changelog


## 2026-11-10 — Issue 250 documentation round

- AGENTS.md describes the delegation, integration and release workflow.
- WORK.md reset to the current round; the earlier bytes are archived on the owner's workspace data volume, not public.

## 2026-11-03 — Issue 201: unknown tool arguments refused

- `tool()` (sync and async) now checks argument names against the live catalogue's input
  schema (fetched once per connection) and raises `ValueError` naming the unknown and the
  allowed names. FontLab drops unknown names silently, so `list_kerning_pairs(master="Bold")`
  used the current master; the parameter is `master_name`. Names only, no type checks; tools
  absent from the catalogue or with open schemas are not checked. `tests/test_argument_guard.py`.

## 2026-11-03 — Issue 201: completeness audit

- Docstrings for every public client method; README API reference (names, error types,
  the client `timeout` versus FontLab's fixed five-second `run_python` deadline, code and
  output size limits); PyPI classifiers, keywords and `py.typed`.
- 33 offline tests (`tests/test_api_surface.py`): every named control, tool paging, error
  paths, timeout fencing, sync-through-portal calls and `run`/`eval`/`execute_script` against a
  fake session that executes the transmitted code. 83 tests pass on mcp 2.3, 1.30.0 and 1.26.0;
  `control.py` 97% and `controls.py` 100% branch coverage. No FontLab contacted.

## 2026-10-15 — issue 104 lane L6 completed (moved from PLAN.md/TODO.md)

- Stdlib-only Glyphs script `glyphs/fontlab_remote.py`: MCP over FontLab's bundled
  `fontlab-mcp` bridge with deadlines on every read; unit tests against the SDK
  fixture server; terminal run against live FontLab; real runs inside Glyphs 3.5.1
  and 4.2 with FontLab responding (fonts, eval); README/CHANGELOG/WORK.
- MCP Python SDK v2 migration (R046 follow-up): `mcp>=1.26,<3`, new `mcp_compat.py`
  (snake_case fields, wire dumps by alias, v1 RootModel unwrap); test fixtures use
  `MCPServer` on v2 and `FastMCP` on v1. Suite: 49 passed on mcp 2.3.0, 1.30.0 and
  1.26.0. Native read-only session (47 tools, run_python, fonts, eval) passes on
  2.3.0 and 1.30.0 (workspace evidence `remopy-mcp2/`).

## v0.2.1 (2026-10-16)

MCP SDK v2 support (mcp>=1.26,<3 via mcp_compat.py), Glyphs-side remote control script, CLI wire-format output, docs and dependency reconciliation (issues 101/104/106). Release review: verification/issue-106/reviews/X5-fontlab-remopy.md.


- 2026-10-15 (review R-mcp2): the `tools` and `call` CLI output uses the MCP wire
  format (camelCase) on both SDK lines; DEPENDENCIES.md states the v1/v2 dependency
  difference correctly.

- 2026-10-15 (R046): DEPENDENCIES.md re-evaluated; superseded the same day by
  the MCP v2 support above (`mcp>=1.26,<3`, `mcp_compat.py`).

- Issue 104: `glyphs/fontlab_remote.py`, a stdlib-only script for Glyphs 3/4 that
  controls FontLab through the bundled `fontlab-mcp` bridge (`tools`, `call`,
  `run_python`, `eval`; deadlines on every read; `isError: null` accepted). Tested
  against the SDK fixture server, from macOS's Python 3.9 and inside Glyphs 3.5.1
  and 4.2 (their Python 3.13) against live FontLab 9.0.9783.

## 2026-10-15 — completed checklist (moved from TODO.md)

- Record source provenance and baseline.
- Implement complete package migration and scoped modernization.
- Verify wheel, sdist, isolated installs and privacy.
- Verify relevant native behavior in FontLab.
- Add reusable ordinary sync/async control and decorated Python functions.
- Verify JSON/results/streams/errors, timeout fencing and process cleanup.
- Pass review and scoped fixes.
- Complete all three project iterations.
- Push, tag, release and verify assets.

## 2.0.4 (2026-11-16)

- Document native UI composition from external Python, including actual TypeRig
  widgets through the existing build callback.

- Preserve Unicode line separators in JSON values, captured streams and native
  exceptions by splitting transport envelopes only on LF; never replay failures.
- Add reusable synchronous FontLab and AsyncFontLab contexts with JSON-native
  eval/run/script results and separate stdout/stderr/native tracebacks.
- Add ordinary @fl.python functions with real signature/default binding,
  metadata preservation, explicit capture/source boundaries and isolated scope.
- Add short fonts()/glyph(name), named native control helpers and live schemas.
- Keep idle sessions alive; fence queued/new calls after timeout/cancellation,
  preserve unknown-outcome notes, and reap SDK bridge processes on cleanup.
- Preserve public NativeExecutionError when it escapes a connection context.

- Extract reusable fontlab_remopy launch, file submission, authenticated native
  MCP discovery/call, verified Python/script execution and MCP setup APIs.
- Preserve actual tool/native errors and unknown timeout outcomes without retry.
- Retain narrow null isError normalization with official SDK message handling.
- Close relay stream channels before teardown and verify child cleanup by PID.
- Preserve current source hashes/licenses in an excluded recovery archive.
- Verify thirteen regressions and live MCP setup/46 tools/.flpy completion.
- Show unknown execution outcomes and retained setup status notes on CLI timeout.

## v0.2.0 publication verified

Actual publication and independent downloaded-asset verification complete.
Three full-project iterations pass; installed tagged wheel/sdist each457tests.
Downloaded native smoke covers all eight packages and both formats, including
production ACP/native UI and TypeRig composition. Exact release URLs, immutable
code commit and asset digests are in RELEASE.md. This follow-up changes only
completion evidence; release code and tag are unchanged.

## 2026-10-15 — workspace plan and checklist reconciliation

Completed repository scope archived after reading WORK.md and checking the
workspace evidence. Workspace release/integration gates remain in the parent
PLAN.md. Historical verification limits below remain part of the record.

### Archived PLAN.md

# Plan

No open work. Issue 101 shipped as v0.2.0; the issue 104 Glyphs remote script and the MCP SDK v2 migration are complete and recorded in CHANGELOG.md.

### Archived TODO.md

# Tasks

No open tasks.


## 2026-11-06 — Issue 233 source/build-only site candidate

Added complete authored site pages, the separate 31-package hash-locked
ProperDocs/MaterialX environment, light fltheme26 controls, generated output and
a main-only two-job build workflow. The read-only job verifies exact source or
direct docs-only child lineage, non-doc identity, the shared source epoch and
full tracked/untracked parity. No Pages permission, request or deployment exists.

Strict builds, all 20 docs tests, actionlint and shellcheck passed. Independent
docs environments rebuilt every output file byte-identically. Real local Git
tests cover changed/unchanged output, foreign staged source, wrong checkout,
missing/unreachable main, stale/concurrent source, hook refusal, immutable lineage
and unexpected ignored output. Cross-date builds retain the original source epoch.
Local Chromium desktop/mobile searches and ordinary result clicks passed;
Escape returns focus to the opener and navigation closes. Dark OS preference
and stored slate remain light. Bulk fill/type event failures and the shared
outside-close focus gap remain disclosed; no WCAG or universal-repeatability
claim follows.

Product source/data, original licences, scripts, runtime locks, recovery pins
and Git refs/configuration remain unchanged. The later freeze found an isolated
index byte-guard exception; staged entries still match HEAD, with no cached
source changes. The cause is not proved. Preserve the current index and use
fresh delivery guards; no old index is restored. Source/generated
patches are local review candidates based on the current source epoch. Independent
review, actual main Actions, fresh-epoch generated delivery, installed/native
acceptance and private P/L remain separate. No product/native suite, owner
installation, commit, push or Pages operation was performed.


## 2026-11-07 — Exact frontend notices and English search assets

Added exact upstream frontend notices and source-map provenance for the existing MaterialX 10.1.8 payload. Explicit English configuration and a small build hook reject language, corpus, reference, asset-set or hash drift before omitting the 35 unused language helpers. All nine retained core assets, original product legal files, guides, catalogue rows, media, runtime and dependency/build locks are preserved.

The strict site build and all 35 documentation tests pass. The complete new hook has 100% statement/branch coverage; real Git staging, checkout and archives preserve exact legal bytes. An independently installed matching lock reproduces all 48 output bytes and modes. Existing immutable source/output, epoch, concurrency and full-parity workflow checks remain active. Browser and independent review evidence are separate from these local checks.

Private Pages configuration, grants, requests and publication remain owner-held; this source follow-up adds none.
No product release or installation is claimed. Prior ordinary artifacts remain bound to their recorded revisions; a later Git revision changes genuine hatch-vcs metadata. Full current source archives include these documentation additions; no unchanged-sdist or whole-wheel identity is asserted. Native acceptance and owner installation remain separate.


## 2026-11-07 — installed icon path-tuple inventory refinement

The current HTML/CSS contains 45 distinct ordered SVG path tuples. A complete scan of the four installed MaterialX icon families finds 43 exact installed matches and two unmatched Lucide tuples, refining the earlier known-candidate inventory. The additional installed match is the Font Awesome version caret-down. Its existing CSS header and full notice retain Font Awesome Free 7.1.0, Fonticons and CC-BY-4.0 icon attribution. The official NPM caret SVG has different raw path bytes; no unmodified-primary SVG, whole-geometry or optimizer-recipe equivalence is claimed. The two unmatched Lucide tuples retain their pinned SCSS source attribution.

A new actual-output regression derives these counts and checks installed matches, unmatched CSS references and the caret header. It fails against the prior 42 count and passes with the corrected metadata. All 36 current documentation tests pass; full strict and independent exact-lock builds match every output byte and mode. Only the legal paragraph, corresponding inventory and legal search row change in the site. Runtime, packaging, generators, vendor assets, full notices, existing guidance and the Fly search fix remain exact. Fresh browser verification and independent review are recorded separately. No private Pages operation, delivery, installed-product upgrade or native acceptance is claimed.
