---
this_file: WORK.md
---

## 2026-11-15 — Shared installer source alignment

Copied the reviewed shared installer exactly: dependency constraints and managed origins remain protected; inactive conditional dependencies are filtered before sibling execution in the resolver target Python. FontLab imports remain standard-library-only. Package identity, runtime APIs, dependency declarations, scripts, bundles and legal files are unchanged. The real source-archive check now includes the exact root installer; the prior omission was reproduced before the single allowlist addition.

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

Remaining work is in PLAN/TODO. Keep the Q5 proprietary metadata/licence
migration, provider checks, fresh artifacts/new release, root installer
completion and installed/native acceptance open. All GUI entries and aliases,
both themes, physical typing, filters, history/Undo/Redo, save/reopen and all
17 Issue 252 native rows still need their evidence. Private Pages, Issue 123's
pause, Book/exclusions and cleanup holds remain. Six inherited expanded Ruff
0.14.10 findings, graph coverage of 113/149 files with 257 unresolved receiver
sites and a 524288-byte cap, UNKNOWN impacts and historical index/control
uncertainty are not cleared. No new artifact, installation or host result is
claimed by this documentation update.
