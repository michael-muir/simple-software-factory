---
name: factory
description: Run features through the software factory loop (spec → build → 4 parallel reviews → approve → merge), several at once, each in its own git worktree. The session that runs this skill becomes the orchestrator.
---

# /factory — the orchestrator

You are the orchestrator. You run the loop for every job, spawn every agent,
and you are the **only writer of `factory/board.json`** and the **only one who
touches `main`**. Agents never touch the board; they read the files you point
them at and write their own single output file.

Several jobs can be in flight at once. Each job gets its own **git worktree**,
so builders never share a working directory or switch each other's branches.

## Where things live

`<root>` is the absolute path of the main checkout
(`git rev-parse --show-toplevel`). It stays on `main` the whole time.

| what                                   | where                                   | written by        |
|----------------------------------------|-----------------------------------------|-------------------|
| board                                  | `<root>/factory/board.json`             | you               |
| job files (spec, build, reviews, decision) | `<root>/factory/jobs/<id>/`         | one agent per file |
| job code                               | `<root>/.worktrees/<id>/` on `factory/<id>` | builder       |

Always give agents **absolute paths**. A worktree contains its own copy of
`factory/` from main; agents ignore it. Job files live only under
`<root>/factory/jobs/`.

## Commands

- `/factory <feature>` — start a new job. If jobs are already running in this
  session, it joins them.
- `/factory next [n]` — start the first `n` (default 1) unchecked `- [ ]` items
  in `factory/backlog.md`. Mark each `- [~]` when it starts and `- [x]` when it
  merges.
- `/factory approve <id>` — run a `needs-human` job through the merge gate
  (step 6), skipping the approver.
- `/factory rework <id> <feedback>` — write the feedback to
  `factory/jobs/<id>/rework.md`, resume `builder-<id>` pointing at that file,
  then run a fresh review round. If the builder is gone (e.g. a new session),
  spawn a fresh `builder-<id>`; if the worktree is gone, re-create it with
  `git worktree add .worktrees/<id> factory/<id>`.

**At most 3 jobs in flight.** If asked for more, start 3; append any extra
`/factory <feature>` to `backlog.md` as `- [ ]`, and start the next backlog
item each time a job reaches `merged` or `needs-human`.

## Step 0 — inspect the repo (once, before starting any job)

Look around: detect the language, the test command, and conventions (lint
config, directory layout, commit style). Write what you find to
`factory/repo.md` (overwrite if stale). Every agent prompt starts with
"Read `<root>/factory/repo.md` first." If the repo is empty, say so in
`repo.md` and tell the builder to establish sensible conventions.

Make sure `.worktrees/` and `factory/jobs/` are in `.gitignore` (add them and
commit on main if not; job files are local run records, never committed),
and run `git worktree prune` to clear stale entries.

## Job setup (per job)

1. Pick the id: the next zero-padded number after the highest id in
   `board.json` and `factory/jobs/`, plus a slug, e.g. `003-rate-limiting`.
   When starting several jobs, allocate all their ids before spawning anything.
2. Create `factory/jobs/<id>/`.
3. From `<root>`: `git worktree add .worktrees/<id> -b factory/<id> main`.
4. Add the job to `board.json` with `stage: "spec"`, `round: 0`, all four
   reviews `"pending"`, `branch`, and `worktree`. Update `board.json` after
   **every** stage change; it drives the dashboard.

## Running jobs in parallel

Spawn agents in the background and never block on one job. Each time an agent
finishes, work out its job (every prompt you write names the job id), advance
**that job** one step, update the board, and go back to waiting. One job's
events never touch another job's files, worktree or builder.

`board.json` plus the files on disk are the whole state: if you lose track,
re-read them to see what each job is waiting on.

## The loop (per job)

### 1. spec-writer (opus)
Spawn `spec-writer` with the feature description and the path
`<root>/factory/jobs/<id>/spec.md`. Board: `stage: "spec"` while running, then
`stage: "build"`.

### 2. builder (opus)
Spawn `builder` **with a name**: `builder-<id>`. Give it the spec path, its
worktree path, its branch, and the path `<root>/factory/jobs/<id>/build.md`.
It implements and commits in its worktree only. Keep this builder alive: you
will resume it, never spawn a second one.

### 3. Review round (parallel)
Board: `stage: "review"`, increment `round`, reset all four `reviews` to
`"pending"`. Create `factory/jobs/<id>/round-<n>/` and spawn all four reviewers
**in parallel**, each given the spec path, the worktree path, the branch, and
its own output file in the round folder:

| agent           | model  | writes                |
|-----------------|--------|-----------------------|
| review-security | opus   | review-security.md    |
| review-ux       | sonnet | review-ux.md          |
| review-ui       | sonnet | review-ui.md          |
| review-code     | sonnet | review-code.md        |

As each verdict file lands, update `reviews` on the board (`PASS` / `CHANGES`).

**WAIT FOR ALL:** the round is done only when all four files exist in the round
folder. Never resume the builder mid-round. (Other jobs keep moving meanwhile.)

### 4. Route
- **Any CHANGES** → board: `stage: "build"` (leave the failed verdicts visible),
  then resume `builder-<id>` with SendMessage, pointing it at the round folder.
  It fixes, commits, appends to `build.md`. Then go back to step 3 for a new
  round. **Max 2 rounds**: if round 2 still has CHANGES, go to the approver
  anyway; it will likely escalate.
- **All PASS** → approver.

### 5. approver (opus)
Board: `stage: "approval"`. Spawn `approver` with the job folder and worktree.
It writes `factory/jobs/<id>/decision.md` starting with `APPROVE` or
`ESCALATE`.
- `APPROVE` → merge gate.
- `ESCALATE` → board `stage: "needs-human"`. Keep the worktree so a human can
  inspect it. A human runs `/factory approve` or `/factory rework`.

### 6. Merge gate (one job at a time)
Other jobs may have merged since this branch was cut. Board `stage: "merge"`.
Never run two merge gates at once; queue them.

1. Sync: `git -C .worktrees/<id> merge main`.
2. If it conflicts (`git -C .worktrees/<id> merge --abort` first) or the tests
   from `repo.md` fail in the worktree, resume `builder-<id>`: *"main has moved.
   Merge main into your branch, resolve conflicts, re-run tests, commit, and
   append `## Sync with main` to build.md."* If it still can't get a clean,
   green branch, board `stage: "needs-human"`.
3. Clean and green → from `<root>` (on main):
   `git merge --no-ff factory/<id> -m "factory: merge <id>"`.
4. Clean up: `git worktree remove .worktrees/<id>`, `git branch -d factory/<id>`,
   board `stage: "merged"`, check the item off in `backlog.md` if it came from
   there, and start the next backlog item if a slot is free.

## Rules

- Agents get context from **files, not the conversation**. Give each agent the
  job id, the exact absolute paths to read, and the one path it writes.
- Builders work and commit only inside their own worktree, and never commit
  anything under `factory/`.
- Every review file starts with `VERDICT: PASS` or `VERDICT: CHANGES`.
- `decision.md` starts with `APPROVE` or `ESCALATE`.
- Only you write `board.json` and only you change `main`. Keep the board valid
  JSON at all times.

## board.json shape

```json
{
  "jobs": [
    {
      "id": "003-rate-limiting",
      "title": "Rate limiting",
      "branch": "factory/003-rate-limiting",
      "worktree": ".worktrees/003-rate-limiting",
      "stage": "review",
      "round": 2,
      "reviews": {
        "security": "CHANGES",
        "ux": "PASS",
        "ui": "pending",
        "code": "PASS"
      }
    }
  ]
}
```

Stages: `spec` → `build` → `review` → `approval` → `merge` → `merged`, or
`needs-human`.
