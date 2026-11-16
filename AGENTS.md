---
this_file: AGENTS.md
---

## Owner priority: functional progress first (2026-11-15)

Future agents must make large, swift advances in working functionality. Prioritize visible user problems and useful, coherent feature increments. This instruction sets the work order and supersedes older requirements to complete exhaustive testing or build test infrastructure before ordinary implementation.

Keep packages coherent and compatible. Check shared APIs, imports and lazy aliases, data formats, dependency direction, object ownership and lifetime, installers, launchers and examples. Update affected providers and consumers together; preserve existing supported behavior and avoid dependency cycles.

During implementation, use the smallest meaningful smoke checks and focused regression tests for the changed behavior and affected package boundaries. Detailed testing, exhaustive coverage, broad performance studies and full acceptance matrices can follow in a later testing pass. Do not let test harnesses, sandbox/supervisor design, repeated unchanged suites, evidence machinery or review paperwork become the main project. Build such infrastructure only when a concrete functional defect or necessary safety constraint requires it.

Record deferred checks and known limits plainly. Do not call untested native, installed or published behavior verified. Keep existing mandatory delivery hooks, preservation rules, licence/privacy obligations, repository exclusions and explicit native/publication holds intact. When one action is held, continue other authorized functional work instead of expanding unrelated infrastructure.

Choose the next substantial useful feature or shared fix and carry its affected providers and consumers together. Timebox supporting investigation; once focused checks establish a usable increment, continue functionality work. Queue detailed testing for a later pass with its concrete remaining checks instead of letting test infrastructure displace product delivery.

## Current scope — 2026-11-05

Issue 230 documentation reconciliation is current. Issue 123 remains paused. The qualified Issue 207 isolated candidate is separate from canonical source, installed artifacts, native acceptance and publication. Reconcile that candidate with later work before integration. Issue 210 specifies future architecture; Issue 211 retains unfinished follow-up checks. Retained dated receipts describe their original source and acceptance surface only.

Canonical source inspected for this proposal: `33a03efbda44`. This is a dated source observation, not an installed or native acceptance claim.

Reconcile caller migrations and Issue 207 distribution changes without removing genuine supported-host or SDK compatibility.

Requalify installed launch/catalogue/nonce execution on the supported host and the App-owned native UI consumer; timeouts do not cancel host code.

## Organization and checks

`src/fontlab_remopy/` contains clients, actions, discovery and MCP compatibility; `examples/`, `glyphs/` and `tests/` hold consumers and checks. App owns the relocated `examples/native_ui.py`.

Run `uv sync --extra test`, `./test.sh`, `uv run --extra test --with "mcp==1.30.0" python -m pytest -q`, and `uv run --extra test --with "mcp==1.26.0" python -m pytest -q`. All three lines are required for the advertised SDK range.

# Agent guidance: fontlab-remopy

## Live font testing in FontLab (owner instruction, 2026-11-10)

Test, verify and edit in the font that is open in FontLab 9. Don't hold back
because the owner might be working on it. Just work in it. If no font is open,
open a VFJ from `~/Desktop` first (File > Open, or `fontlab.flPackage(path)`
and `flWorkspace.instance().addPackage`). Those VFJs are for agents. Add glyphs,
kerning pairs, elements, contours, masters or anything else the test needs,
and save the files when that helps. This replaces older rules that required an
empty FontLab session or forbade editing open fonts. `fl-native.sh --mutating`
now runs with fonts open (`FL_REQUIRE_EMPTY=1` restores the old check). The
serialized lock still applies: one native run at a time. Don't quit or restart
FontLab, and don't close fonts from Python, because that has crashed the host.

`fontlab_remopy`: launch, script execution and authenticated MCP remote control of FontLab, plus a stdlib-only Glyphs script (`glyphs/fontlab_remote.py`). Read the workspace AGENTS.md and DECISIONS.md first; this file adds repo rules only.

## Rules

- No AI libraries or agent prompts here; those belong to Aidus. Dependencies stay `mcp>=1.26,<3` and `anyio`.
- Must run on both MCP SDK lines. Version differences live only in `mcp/compat.py`. CLI `tools`/`call` output uses the MCP wire format (camelCase) on both.
- `glyphs/fontlab_remote.py` stays standard-library only and runs on Glyphs' Python (README claims 3.8+; tested on 3.9 and 3.13). Every read there has a deadline.
- A timeout leaves the outcome of a mutation unknown. Never retry automatically; never replay an operation after a decoding failure. Calls are serialized; after timeout/cancellation the context refuses new calls until reopened.
- Never clear native Output. `Remopy.output()` reads the MCP log; `Fontlabapp.output()` reads the native panel; different surfaces.
- First-party source and documentation use Apache-2.0; retain NOTICE and third-party terms. MIGRATION.json records historical recovery digests; no recovery archive is present in this checkout. Preserve the frozen MIGRATION.json hashes; do not recreate or relicense that archive.

## Commands

- Tests, locked SDK 2.x: `./test.sh` (= `uv run --extra test python -m pytest "$@"`). Other lines: `uv run --extra test --with "mcp==1.30.0" python -m pytest -q` and `--with "mcp==1.26.0"`. Run all three before claiming SDK compatibility. Build: `uv build`.
- Host-side environments: arm64 Python 3.11 (`cpython-3.11-macos-aarch64-none`; check `lipo -archs`). An x86_64 3.11 needs `cryptography<47` and cannot be loaded by arm64 FontLab.
- Native runs only through `verification/issue-104/fl-native.sh`.

## Host rules that apply here

- `run_python` has a fixed 5 s deadline, 32768-byte code and 65536-byte output bounds. A client timeout does not stop host execution: a runaway loop pins FontLab's main thread. Anything that can reach user or corpus code needs its own in-FontLab deadline; clients leave via `os._exit` when the host is busy.
- Code started on the event loop (`QTimer.singleShot`, deferred exec) outlives the call that scheduled it.
- Never call `PyThreadState_SetAsyncExc(thread_id, NULL)`: it permanently sets the eval-breaker and hangs the next traced call (FontLab 9.0.9783).
- Never `close_font` while FontLab shows that package's "Save Changes?" dialog. Close owned copies with `close_font(font_id=..., save=False)` in `finally`.
- After a crash FontLab shows a Crash Report dialog and MCP stays down until it is dismissed; after a kill with open documents it blocks on "Restore Autosaved Fonts". Neither is visible to System Events while the screen is locked. Remove only agent-owned autosave files, never the owner's.
- Do not mutate even owned in-memory packages in the user's live FontLab (queued notifications crash it, e.g. on Preferences Apply). Native mutation needs a document-free dedicated session, then a restart.
- Native tests use owned fixtures only; never user-open fonts, preferences or the Output panel.
- For `@fl.python` bodies and [App's `examples/native_ui.py`](https://github.com/fontlabcom/fontlab-fontlabapp/blob/main/examples/native_ui.py): native PythonQt instances reject new attributes; `bytes(QByteArray)` raises (use `.data()`); disconnect every signal before `deleteLater()`; never `disconnect` a receiver holding both a native-slot and a bound-method handler (segfault).

## Proof and git

- Offline tests and SDK fixture servers are not native proof. Installed-artifact checks run inside FontLab.
- The canonical checkout is editable-installed into the owner's FontLab: preserve it and use an isolated successor for the current task. Do not move or re-create `v0.2.*` tags.

## Milestones and delivery

Read [PLAN.md](PLAN.md), [TODO.md](TODO.md) and [WORK.md](WORK.md) before work.
Make the smallest complete MVP for one named acceptance task. Find all callers,
tests, fixtures, exports and documentation first. Use graph impact before source
symbol edits; confirm stale or unknown graph results against current source.
Keep product work in isolated successors and preserve the owner's checkout.

Run this repository's exact checks and the unchanged 80% gate for each complete
changed production module. Use an independent review before a milestone commit.
Under the current owner task, commit and push reviewed, passing milestones;
verify remote heads rather than inferring delivery from local tracking refs.
Before main integration, reconcile concurrent work and all consumers, run graph
change analysis and repeat the required acceptance on the combined source.

Before removing obsolete branches or files, prove integration, retain recoverable
unique work and check fresh owner/worktree attachments. Preserve sealed reports,
licences, archives and private data. Do not rewrite history by implication.
Remove verified completed work from PLAN/TODO and record scoped evidence in
CHANGELOG. Keep implemented-only native/artifact checks open in TODO. Issue 123
remains paused; no instruction here authorizes driving the owner's FontLab,
installing into its user folder or publishing a site.

## Issue 233 source/build-only documentation

Maintained site source is `src_docs/md`, configured by `src_docs/mkdocs.yml`;
`docs/` is generated output. Use a separate Python 3.13 docs environment, uv
0.13.7 and the exact hash-locked requirements. Run `sh src_docs/build.sh` and
`python -m unittest discover -s tests_docs -v` with that environment on PATH.
Every main push builds exact source X, optionally makes a normal docs-only child
Y, and independently verifies immutable lineage, source identity, source epoch
and complete tracked/untracked generated parity. No private Pages permission,
configuration, deployment or automatic publication request is enabled.
Source/generated review, actual Actions, owner installation and native acceptance
remain separate. Do not change runtime dependencies, startup or recovery pins for
a site build.

## Integration rounds

After each round of important changes, integrate it into `main` and upstream:
fetch `origin/main`, build the change on top of it in an isolated branch or
worktree, and resolve conflicts by keeping both our work and teammates' work.
Never discard upstream commits, and never force-push. Run the repository's
checks on the merged result, then push to `origin main`. Record the change in
CHANGELOG.md, move verified-solved TODO.md items into CHANGELOG.md, update
PLAN.md, and continue with the next TODO.md item until the list is clear.
`install.vfpy` is shared: keep it byte-identical in every installer repository.

## Verified integration rounds — 2026-11-10

After each important independently reviewed round, recheck actual upstream
`main` and owner/worktree attachments. Fetch in a new isolated successor based
on current `origin/main`, merge the round's reviewed work, and resolve conflicts
by preserving both sides' intent, newer fixes and teammates' changes. Preserve
owner checkouts, branches, indexes, refs and configuration; never pull, switch
or rebase an owner's or another agent's active worktree. Stage only the exact
reviewed residual delta. Run the repository's applicable full suite, lint and
graph change gates on the combined tree, obtain independent merge review, then
commit and push under the current owner task's authority. Keep required hooks,
including the installed Dismisser pre-push gate, active; never bypass them or
force-push or rewrite history. Verify the actual remote head and required
main-triggered Actions; a local tracking ref is not delivery proof.

Move only evidenced solved tasks from future PLAN/TODO into cumulative
CHANGELOG, retaining every unrelated entry and placing new progress first. Keep
TODO flat and unchecked, update PLAN to remaining work, and continue the next
authorized task. Unverified native, SDK, UI, history, artifact, adoption and
publication checks stay open. The workspace root remains non-Git. Preserve
excluded repositories, recovery, licences and private data; this workflow does
not authorize FontLab installation or native operations, resume Issue 123, or
lift private Pages holds. Native upstream fixes use reviewed PRs to the
cause-appropriate Proteus, FontGate or pyfontgate repository.

## Isolated successors

Overrides generic bootstrap/MCP.

For graph work in an isolated successor, use the qualified installed CLI or backend with both `GITNEXUS_HOME` and `GITNEXUS_STORAGE_PATH` set to separate task-owned locations before the first invocation, including index discovery and analysis. A private storage path alone can still register the successor in global control files. During ordinary analysis, do not fall back to global MCP defaults, global `list-repos` or global setup/bootstrap, and do not make unreviewed global registry edits. Retain exact command/selected environment and before/after owned metadata; record expected task-owned `.git/info/exclude` additions and preserve unrelated state. If discovery or indexing escapes the owned scope, preserve evidence and obtain independent bounded control-file review before integration. Any necessary recovery must be separately reviewed, use fresh guarded current bytes and reviewed writer coordination, and change only the proven task-owned entry while preserving all other current records and bytes; never restore an old whole global registry.

## Agent workflow (Issue 250, 2026-11-10)

- Plan with `superpowers:subagent-driven-development`: one fresh implementer per task, a separate read-only reviewer, then the controller runs the gates and commits.
- Send bulk, well-specified work to Codex via the `codex-delegate` skill (`node ~/.agents/skills/codex-delegate/scripts/relay.mjs --brief BRIEF --cd WORKTREE`, in the background). Use `claude-delegate` or `cursor-delegate` for second opinions or independent lanes. Delegates never commit, push or tag.
- Work in a fresh worktree of `origin/main` on the workspace data volume; never pull, switch or reset the owner checkout. Merge `origin/main` again before pushing, keep both sides' CHANGELOG/PLAN/TODO entries, rerun the full suite, lint and graph change analysis, push through the pre-push hook where one is installed (never force), verify the remote SHA and the CI run where a workflow is configured. Held private Pages operations (workspace D41) stay held.
- Release: tag the next semver above the latest tag and publish a GitHub release. Install released, gated packages into `~/Library/Application Support/FontLab/FontLab 9/` and test live in FontLab 9. This owner route (Issue 250) supersedes, for released packages only, every older line in this guide that forbids installing into the FontLab user folder or its site-packages, owner-managed editable installs, or starting FontLab for a live test (the owner's canonical editable checkouts themselves stay owner-managed): record the previous installed distribution first so it can be restored, and never touch FontLab preferences (owner fonts and documents: see live font editing below); native work goes through the workspace `verification/issue-104/fl-native.sh` gate.
- Documents: CHANGELOG holds verified completed work; TODO only open or to-verify items; PLAN the major remaining changes; WORK.md the current round only (older WORK bytes are archived on the owner's workspace data volume, not public).
- Native defects: issues at github.com/fontlab/fl; fixes as pull requests to fontlab/Proteus, fontlab/FontGate or fontlab/pyfontgate. Never commit to the local C++ snapshot.
- Older "work directly" or "no delegation" lines in this guide are superseded by this section (Issue 250).
- Live font editing (owner, 2026-11-10; workspace D44): test, verify and edit the font open in FontLab 9, and do not stop because the owner might be working in it. Open a VFJ from `~/Desktop` first (those files are for agents), then add glyphs, kerning pairs, elements, contours, masters or whatever the test needs, and save them freely. This supersedes, for live testing, every older line here that forbids mutating owner fonts or documents or requires owned fixtures only. FontLab preferences, Output folders and global update queues stay untouched. Keep the serialized host lock (`fl-native.sh`, one native run at a time; `--mutating` now allows open fonts); do not quit or restart FontLab and do not close fonts from Python, which has crashed the host.
