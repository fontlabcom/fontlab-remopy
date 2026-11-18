---
this_file: PLAN.md
---

## Issue 274 startup readiness: remaining acceptance

Qualify real macOS cold-start/disabled-MCP readiness on a bridge-capable build
through the prescribed serialized native runner, and qualify native Windows
launch/submission separately. The installed build 9813 bridge crash and missing
prescribed runner currently prevent native admission. A startup modal that blocks
file submission needs manual dismissal; the once-only setup macro cannot suppress
it before executing. Keep existing native holds. Published provider/consumer,
ordinary resolver and docs-successor checks are recorded in CHANGELOG.

## Issue 271 installer qualification

Integrate the independently reviewed generated installer through existing full
repository/hook gates; verify exact-SHA CI and archives, then qualify native
macOS/Windows use when the serialized guard is available. Preserve owner files.


## Guarded common installer: remaining qualification

Obtain independent final review of the canonical 1.0.11 template and static
oracle, verify the current graph and reconcile with actual upstream main.
Qualify the ordinary push hook, exact-commit CI and release/archive/download
inputs on that final source. Repeat the required three-SDK checks if the source
or dependency tuple changes. Source suites and local fixture servers do not
qualify consumer installation, owner recovery or native/Windows receipts.
Keep the full provider/consumer cohort, Aidus/Fly adoption, unknown Windows replay
and private Pages gates open under their existing admission rules.


## Issue 256 Windows submission: remaining qualification — 2026-11-17

Independently review the explicit CrossOver/Wine launch and submission candidate,
reconcile with fresh main, run ordinary combined-source and hook gates, and verify
remote delivery and exact-SHA CI. Admit real CrossOver/Windows receipt-backed
execution only through the serialized native guard. Qualify Windows standalone
Python/uv bootstrap, wheel installation, embedded imports and native MCP discovery
separately; offline command construction and submission cannot establish them.

## Shared installer: remaining delivery qualification — 2026-11-15 (same candidate as the guarded common installer above)

Reconcile the source-reviewed, three-SDK-qualified shared-installer candidate against fresh main, obtain independent merge review, run normal hook/combined-source gates, verify main delivery and exact-SHA CI, then qualify the tag/release/archive/download inputs. Preserve the existing package-specific dependency and distribution contracts. Then qualify the coherent provider/consumer and Script/Extension cohort through the admitted root installer and native lane; source checks do not establish those outcomes. Keep every existing ownership, native, publication and paused-work limit.



# Forward plan

## Remaining archive and native qualification

Remopy 2.0.2 source/legal metadata, ordinary release/downloads and bounded
installed-wheel checks are qualified in CHANGELOG. Resolve the original archive
contract separately; historical recovery is absent from this checkout and is
not relicensed. Preserve the historical 149-file raw-mode FAIL, frozen
MIGRATION.json hashes, third-party terms and the private Pages hold. Complete
actual root-installer/FontLab/native acceptance under the existing admission rules.
## Functional work order — 2026-11-14

Prioritize reliable supported-host launch, catalogue and command execution with the current App and Aidus consumers. Keep advertised MCP SDK compatibility and the retained deprecated entry point intact; preserve serialized calls and unknown mutation outcomes after timeouts.

Use small smoke checks and focused regressions for changed behavior and package boundaries. Keep the existing detailed acceptance tasks for a later testing pass; mandatory delivery hooks and current holds remain in force.

Issue 230 reconciliation is current. Issue 123 implementation remains paused; its acceptance backlog below is preserved, not resumed. Keep qualified Issue 207 candidates distinct from canonical source, ordinary installed artifacts, native acceptance and publication. Issue 210 defines the future plugin split; Issue 211 retains follow-up checks. The owner corrected the preparation catalogue reference to Issue 214.

## SDK and source tuple

Preserve the qualified three-SDK checks (locked2.x,1.30.0,1.26.0); rerun affected checks when source or supported providers change. The old issue122 worktree-only instruction is historical, not a requirement to recreate that checkout. Preserve supported SDK/host compatibility while reconciling Issue207 caller/distribution cleanup.

## Installed native acceptance

After owner access restoration, audit the actual process/build/documents/dirty state and fences before native qualification. Recheck installed-artifact setup, catalogue, nonce-verified `.flpy` execution and launch on the current FontLab build. Use owned fixtures through the workspace native runner. Offline transports/fixture servers do not prove a native host; timeout is not cancellation.

Requalify [App's examples/native_ui.py](https://github.com/fontlabcom/fontlab-fontlabapp/blob/main/examples/native_ui.py) against the actual current App/Remopy refactor, including TypeRig composition, ownership, cleanup and complete-font preservation. Do not recreate the removed duplicate in Remopy. Keep artifact/origin, native, promotion and publication gates separate.

## Development checks

Run `uv sync --extra test`, `./test.sh`, `uv run --extra test --with "mcp==1.30.0" python -m pytest -q`, and `uv run --extra test --with "mcp==1.26.0" python -m pytest -q`. All three lines are required for the advertised SDK range.

## Review, integration and cleanup

Use the detailed open tasks in [TODO.md](TODO.md) as the acceptance checklist. Complete one scoped MVP, then run the exact repository checks and unchanged 80% gate for each complete changed production module. Keep source, genuine artifacts, ordinary origins and native behavior separate. Obtain independent review before a milestone commit/push and verify the actual remote head. Reconcile concurrent source and all callers before main integration. Preserve recovery/unique work and fresh owner/worktree attachments before obsolete branch/file cleanup. Update TODO/PLAN and record only scoped verified results in CHANGELOG. Do not drive the owner's FontLab, install into its user folder or publish a site from this proposal.

## Documentation delivery gates

Obtain independent review of the complete source and generated site, preserve
current source bytes, then qualify exact-SHA main Actions through the ordinary
reviewed delivery process. Exercise changed-output bot-child and code-only live
triggers separately. Private Pages publication remains owner-held.
