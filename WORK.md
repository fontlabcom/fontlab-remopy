---
this_file: WORK.md
---

## 2026-11-19 — Public script-first MCP setup

`ensure_ready()` now validates the selected bridge and directly calls the public
`setup_mcp()` operation. Its `.vfpy` file opens FontLab, enables MCP and hides
warning dialogs before any MCP probe. The separate launch/initial-probe branch
is removed. Existing fontlab-cli tools/eval/run/call hooks use this path; user
operations are not replayed. README/site show explicit public setup usage.

The controller submitted the True-preference macro once through existing Remopy
file submission; its nonce-matched native marker confirms success and
`generalHideWarningDialogs = True`. This proves the preference script itself;
the independently failing native bridge eval is a separate connection outcome.

All three SDK suites pass 257 tests without skips (20.29/17.60/17.59 seconds),
with one existing deprecation warning each. The three removed parameter cases
covered the deleted conditional initial-probe branch. Tests assert setup before
any probe and require the actual macro's marker before catalogue discovery.
Scoped Ruff, strict locked docs generation and all 37 docs tests (8.996 seconds)
pass. Commit/publication remain controller-owned for the next 2.0.13 patch.

## 2026-11-19 — Issue 274 published provider/consumer delivery

Remopy 2.0.12 was published to GitHub and PyPI from runtime source
`2ed7cd298b488c013a27c3761d9550c795379dfd` through successful release run
[44418837873](https://github.com/fontlabcom/fontlab-remopy/actions/runs/44418837873).
The consumer's `fontlab`, `fontgate` and `fontpr` 1.0.2 packages were published
from `3cb604419516ab068a92ebbf938a614e43f126b3` through successful release run
[44419239311](https://github.com/Fontlab/fontlab-pypi/actions/runs/44419239311);
all six consumer OS/Python CI combinations passed.

The initial Remopy documentation run failed because the API contract expected
11 rows after README added the twelfth row. Docs-only successor
`18008026b4d34f2a2815bb097567eb7b017a1420` corrected the contract and site source,
passed the unchanged ordinary hook (260 tests, 28.93 seconds), and became the
verified remote main. Controller strict generation and all 37 docs tests passed
in 7.034 seconds. Exact-successor documentation run
[44419786100](https://github.com/fontlabcom/fontlab-remopy/actions/runs/44419786100)
succeeded. The runtime release source and v2.0.12 tag remain unchanged; this
successful docs run qualifies the successor, not the original runtime commit.

Independent released-artifact verification installed all three consumer packages
from PyPI through ordinary dependency resolution and selected Remopy 2.0.12.
`uv pip check` passed; all eight downloaded wheel/sdist SHA-256 values agree
across PyPI and GitHub, and installed production bytes match the released wheels.
The released SDK fixture passes tools/eval/run/call with exactly one confirmed
setup submission and no user-operation replay. This supersedes the candidate
wheel dependency-floor limitation; the detailed release verification remains in
external task evidence.

Native acceptance remains open. The installed /Applications build 9813 has the
known bridge crash, and the prescribed serialized native runner is unavailable,
so no native admission or owner installation occurred. Real macOS cold start,
startup-modal behavior and native Windows execution remain unverified. The
previous WORK bytes were archived and verified before this entry was added.

## 2026-11-19 — Issue 274 docs contract follow-up

The main documentation check still required 11 API rows after README added
`ensure_ready`; the actual site source also omitted that row. The check now
requires exactly 12 rows and explicitly names `ensure_ready`, retaining every
existing rendered-row and normative-session assertion. The API and installation
pages describe native Windows support, bounded readiness, once-only setup,
persistent warning suppression and startup-modal/bridge limits.

The revised regression failed against the previous generated HTML, then passed
after rebuilding. With uv 0.13.7, Python 3.13.18 and the exact hash-locked docs
requirements, `sh src_docs/build.sh` passed strict clean generation and
`python -m unittest discover -s tests_docs -v` passed all 37 tests in 7.125
seconds. Generated changes are limited to the two corrected HTML pages and the
search index. No runtime, dependency, release tag or native state changed.
Ordinary docs integration and exact-SHA CI remain controller-owned. The previous
WORK bytes were archived and verified before this entry was added.

## 2026-11-19 — Issue 274 startup readiness source candidate

Added synchronous `ensure_ready(app, command, timeout)` for native macOS and
Windows. It launches once, checks the authenticated catalogue, and submits one
nonce-confirmed setup macro only when the bridge reports an unavailable host.
The macro enables external MCP and persists `generalHideWarningDialogs = True`.
Read-only catalogue probes share the full remaining startup deadline; user
operations are never retried. A failed or unconfirmed setup retains its files.
Windows paths remain individual process arguments; setup source is UTF-8.

The controller's unchanged `quality.sh` gate passed all 260 tests with no skips
and one existing deprecation warning in 36.11 seconds. All six complete changed
production modules exceed the 80% gate: setup 96.36%, compatibility 95%, and the
other four 100%. Controller SDK 1.30.0 and 1.26.0 suites each passed 260 tests
with no skips and the same warning in 17.08 and 17.09 seconds. A task-owned App
sibling link permits the existing AST-only consumer check without executing App.
Unicode-path setup is covered under a simulated Windows cp1252 locale.

Independent source review, installed-wheel fixture verification and the final
AI-slop pass are clean. The installed fixture exercises actual SDK transport and
all four consumer CLI remote routes without launching FontLab. Task-owned graph
analysis completed; its untraced entry points, skipped callees, unresolved receiver
sites and file cap remain explicit limits in the independent verification report.
Ordinary main/artifact delivery and native acceptance remain separate. The
previous WORK bytes were verified into the external task evidence archive before
this entry was added.

No native process, installer or preference was touched. The known build 9813
bridge crash remains a native limit. A modal startup dialog can prevent the
first macro from running; the API times out rather than replaying it. No native
startup argument for suppressing such dialogs was found in the inspected source.

## 2026-11-18 — Issue 271 generated installer candidate

Regenerated `install.vfpy` with Instamix 1.0.18, preserving project declarations and
runtime source. Exact reviewed-template byte parity and import-sentinel/wheel-order smoke checks pass. Existing focused installer tests pass (exit 0, 0.62 seconds).
Task-owned graph impact/change analysis cannot resolve an index; structural caller
checks supplement this unavailable evidence. Full repository delivery gates,
independent cohort review and native qualification remain pending. No owner install ran.


## 2026-11-17 — Guarded common installer source qualification

The installer validates the requested FontLab data context before reusing an
installed provider. Reuse requires the migration, message and failed-upgrade
rollback entry points; a provider missing these capabilities must be refreshed.
The copied bootstrap is the exact canonical Instamix 1.0.11 template. Legacy
rollback requires 1.0.9 or newer; context guarding originated in 1.0.10, and
shared-layout venv reuse requires 1.0.11. Package metadata, dependency floors,
runtime code, scripts, bundles and licences are unchanged.

In a fresh full checkout, the complete source suite passed on project-resolved
MCP 2.3.0, MCP 1.30.0 and MCP 1.26.0: 235 tests each, no skips, one retained
deprecation warning each, in 28.28, 25.07 and 24.80 seconds. These runs use local
SDK fixture servers and mocked host submissions. App's sibling UI example is
AST-read only; the common installer template is read as plaintext. No installer,
App, Fly or Instamix provider was executed. A separate unchanged normal-hook run
on the same runtime, installer and test bytes passed 235 tests in 28.69 seconds,
with no skips and the same warning. It found zero changed production modules;
that result makes no changed-module coverage claim.

Independent final review, current graph qualification, actual main integration,
exact-commit CI and release inputs remain separate gates. Documentation checks,
installed provider/consumer coherence, owner recovery and native/Windows receipt
acceptance are separate from these source tests. Existing consumer-execution,
Aidus/Fly, unknown Windows replay, private Pages and paused-work holds remain.


## 2026-11-17 — Issue 256 Windows submission source candidate

Added explicit CrossOver and ordinary Wine launch/submit providers and CLI backend
selection. Executables derive single-separator C: paths from the selected drive_c;
Wine scripts remain drive_c-only. CrossOver uses an absolute validated private
bottle selector, supported by the installed launcher's CXBottle::find_bottle,
to avoid selecting a different configured BottlePath. Existing macOS/export/MCP
contracts remain unchanged. TimeoutExpired reports unknown outcomes; no retry.

Focused regressions initially failed for missing providers/CLI routes (39 failed,
5 passed). The first implementation passed 67 boundary tests. Two additional
red regressions exposed Windows drive/separator characters in native filenames;
conversion now refuses those names before process execution. Final locked, MCP 1.30.0 and MCP 1.26.0 suites each pass 235 tests
(19.56/18.06/17.18 seconds), with one existing deprecation warning. Complete
changed-module combined coverage is CLI 94%, CrossOver 100%, Wine 100%. Scoped
Ruff and the genuine hatch-vcs build pass. Independent review remains pending. No FontLab,
Wine/CrossOver process, installation, commit, push or release ran. Native Windows
and Windows uv/bootstrap qualification remain open above the source checks.

## 2026-11-15 — Shared installer source alignment

Copied the reviewed shared installer exactly: dependency constraints and managed origins remain protected; inactive conditional dependencies are filtered before sibling execution in the resolver target Python. FontLab imports remain standard-library-only. Package identity, runtime APIs, dependency declarations, scripts, bundles and legal files are unchanged. The real source-archive check now includes the exact root installer; the prior omission was reproduced before the single allowlist addition.
## 2026-11-14 — Functional work order documented

Updated AGENTS, PLAN and TODO to prioritize useful functional changes and compatible package boundaries, with detailed testing deferred. Existing backlog and prior records are retained. Documentation preservation and policy consistency were checked; no runtime, installed or native checks ran in this documentation-only pass.

Next: reconcile launch/catalogue/command changes with App and Aidus consumers and supported MCP SDK paths using focused checks before the detailed installed-host pass; never replay an unknown mutation.

Nothing is in progress. Remopy 2.0.0 is on `main` (eight deprecated modules removed). Completed work is in CHANGELOG.md; open work is in TODO.md and PLAN.md.

Fresh isolated successor: the eight reviewed source postimages were hash-verified before transfer; the approved AGENTS priority amendment is separate. Independent source review passed. Focused archive/layout checks pass on Python 3.11 arm64 (9 passed). Controller full-suite checks passed on locked SDK, MCP 1.30.0 and MCP 1.26.0: each 179 passed with one existing missing-App-sibling skip, in 21.66/26.07/26.61 seconds pytest time (22.05/26.78/27.03 seconds command elapsed). The lock remains byte-exact. The older attempt remains held; historical graph scope and control-state uncertainty remain open. Normal hooks, fresh-main merge and independent merge review, main delivery/CI, tag/release/downloads, installed provider closure and admitted FontLab/native/full-cohort workflows remain pending. No owner-folder installation or native operation ran.



## 2026-11-14 — Remopy 2.0.2 Apache release qualified

[Remopy v2.0.2](https://github.com/fontlabcom/fontlab-remopy/releases/tag/v2.0.2) binds source/main `00d200b8924e5663e513f6f545882ec9bb4ef27a`; annotated tag object `5ce9244f53300a0ccddac6a64c4de28faa1a66fd` peels to that source. The unchanged ordinary main hook passed 179 tests without skips in 31.06s, with all 16 production modules at least 80% combined coverage; the ordinary tag hook passed 179 tests in 30.55s. Exact-source CI43646468359 passed both 37-test documentation jobs with SOURCE==OUTPUT==that commit.

The two published assets were actually downloaded. Wheel SHA-256 `b320677b15eea41f53eec38393a1a9631a2ae728f18056c0c572d7fb7dcc16e8`; sdist SHA-256 `26205280fd20cb3513d565e3eb75c41b30626621eec535d582cdf43b37057030`. Current first-party source/docs and legal metadata use owner-authorized Apache-2.0; 47 inserted headers preserve runtime ASTs, third-party bytes/notices and frozen MIGRATION.json. All 17 runtime files and installed RECORD validate in a fresh prefix from the downloaded wheel; 78 transport/SDK/API tests passed in 11.05s with one warning and no native providers. Earlier three-SDK runs retain 178 passes and the missing-App-sibling skip; a real-App focused check passed six tests, and the final hook passed without that skip.

Independent postpublication REMOPY-RELEASE-REVIEW.md approves these bounded source/release/download/prefix results. The original archive contract and T17 remain open; the historical 149-file raw-mode FAIL is retained. Root install.sh, FontLab installation/native behavior, history/save-reopen, private Pages and cleanup were not performed.

The earlier source-candidate and repair notes below are historical; their pending release/licence wording does not describe current 2.0.2. This four-ledger update awaits independent review and controller delivery.

# Apache licensing source candidate — 2026-11-14

The owner authorized Apache-2.0 for Remopy first-party source and documentation.
Updated LICENSE, retained the 2025 Fontlab Ltd. copyright in NOTICE, changed
package metadata and included both legal files in wheel/sdist. Added SPDX
comments to the 47 tracked authored Python, shell and vfpy files. Original
bytes remain intact after removing the inserted comments; runtime ASTs match.
The existing layout test module adds one actual wheel/sdist legal-payload test.

Corrected stale claims that the recovery archive is present in this repository;
no recovery archive is present in this checkout and historical bytes are not
relicensed. MIGRATION.json and all third-party
frontend bytes, maps and notices remain unchanged. The source licence page and
its generated payload reflect the first-party terms. Added the exact shared
functional-priority instruction block. No runtime logic changes.

Baseline: 177 passed, one existing skip and one warning (20.35 s). The new
actual-wheel/sdist legal test failed on the old proprietary expression, then
passed after migration. Final locked SDK, MCP 1.30.0 and MCP 1.26.0 runs each
passed 178 tests with the same skip and warning (20.85/17.54/17.42 s). The skip
requires the absent App sibling checkout; the warning is the tested deprecated
mcp_bridge alias. The first candidate shell run returned 127 after the running
shell reread test.sh during header insertion; its pytest run passed, but that
shell result was a failure. The final locked run completed with exit 0.

The exact locked Python 3.13 docs environment passed the strict build and all
37 docs tests (7.415 s). After the final recovery wording correction, the strict
build and seven actual-output site tests passed again. Generated vendor bytes
and maps, MIGRATION.json and tracked modes match the preimages. All 47 header
insertions preserve the previous bytes; 42 Python/vfpy ASTs match their
pre-insertion bodies and 41 match the base (the layout test adds the regression).
Genuine hatch-vcs wheel/sdist build passed; this is a dirty source candidate,
not a release. The controller retains the independent review/delivery gates. No commit, release,
installation, native operation or private Pages publication is claimed.

## Earlier delivered documentation repair


Independent review approved source/main delivery of
[aab6906](https://github.com/fontlabcom/fontlab-remopy/commit/aab6906aba43404eccbb584b39b0d1a4d27506ad),
tree `32a4b2f29156728cf61480e86af949286c15f78c`. The exact five-file
repair retained the prior assertions and passed the five-state Git regression,
37 docs cases, all three 178-case SDK contexts and the strict 48-file build.
All 16 runtime modules exceeded 80% combined coverage (minimum 84.06%, package
95.49%). These remain source checks, separate from native behavior.

The unchanged installed pre-push hook passed 178 tests with one existing
warning in 28.18 seconds; the ordinary push took 33.89 seconds. Zero changed
production modules means no hook coverage claim. The earlier detached-checkout
push failed before tests; a new owned tracking branch at the same commit/tree
supplied the actual upstream baseline without changing an owner branch or
bypassing the hook.

[Documentation run 43581035677](https://github.com/fontlabcom/fontlab-remopy/actions/runs/43581035677)
passed build and qualification on attempt 1. Generated-only child
[58f30ba](https://github.com/fontlabcom/fontlab-remopy/commit/58f30ba1fde71e11389c37044f36a336ea0f1760)
has sole parent aab6906, changes only two sitemaps and qualifies 48 generated
payloads at source epoch 1794648574. Four controller phases preserved the
captured owner admin/index, all 149 tracked identities, refs and attachments.
Git-archive modes are not checkout raw-mode proof. No private Pages request ran.

Only the repair's solved delivery follow-up is removed from PLAN/TODO. The
complete previous WORK.md is archived byte-for-byte with its raw mode and hash
in private task evidence; older archive references remain in those bytes.
This progress update has not yet been independently reviewed or delivered.

Remaining work is in PLAN/TODO. Provider checks, fresh artifacts/new release, root installer
completion and installed/native acceptance open. All GUI entries and aliases,
both themes, physical typing, filters, history/Undo/Redo, save/reopen and all
17 Issue 252 native rows still need their evidence. Private Pages, Issue 123's
pause, Book/exclusions and cleanup holds remain. Six inherited expanded Ruff
0.14.10 findings, graph coverage of 113/149 files with 257 unresolved receiver
sites and a 524288-byte cap, UNKNOWN impacts and historical index/control
uncertainty are not cleared. No new artifact, installation or host result is
claimed by this documentation update.
