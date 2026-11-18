---
name: factory
description: Run a feature through the software factory loop (spec → build → 4 parallel reviews → approve → merge). The session that runs this skill becomes the orchestrator.
---

# /factory — the orchestrator

You are the orchestrator. You run the loop, spawn every agent, and you are the
**only writer of `factory/board.json`**. Agents never touch the board; they only
read the files you point them at and write their own single output file.

## Commands

- `/factory <feature description>` — run a new job through the loop.
- `/factory next` — take the first unchecked `- [ ]` item in `factory/backlog.md`,
  run it as a job, and check it off (`- [x]`) when it merges.
- `/factory approve <job-id>` — merge a `needs-human` job's branch into main and
  set its stage to `merged`.
- `/factory rework <job-id> <feedback>` — write the feedback to
  `factory/jobs/<id>/rework.md`, resume the job's builder pointing at that file
  (if that builder no longer exists — e.g. a new session — spawn a fresh
  `builder-<id>`), then run a fresh review round.

## Step 0 — inspect the repo

Before the first job, look around: detect the language, the test command, and
conventions (lint config, directory layout, commit style). Write what you find
to `factory/repo.md` (overwrite if stale). Every agent prompt below starts with
"Read `factory/repo.md` first." If the repo is empty, say so in `repo.md` and
tell the builder to establish sensible conventions.

## Job setup

1. Pick the next job id: zero-padded number + slug, e.g. `003-rate-limiting`.
2. Create `factory/jobs/<id>/` and branch `factory/<id>` off main.
3. Add the job to `board.json` with `stage: "spec"`, `round: 0`, and all four
   reviews `"pending"`. Update `board.json` after **every** stage change — it
   drives the dashboard.

## The loop

### 1. spec-writer (opus)
Spawn the `spec-writer` agent with the feature description.
It writes `factory/jobs/<id>/spec.md` (with acceptance criteria).
Board: `stage: "spec"` while running, then `stage: "build"`.

### 2. builder (opus)
Spawn the `builder` agent **with a name**: `builder-<id>`. Point it at `spec.md`
and the branch. It implements on the branch, runs the tests from `repo.md`
against the spec's acceptance criteria, commits, and writes
`factory/jobs/<id>/build.md`.
Keep this builder alive — you will resume it, never spawn a second one.

### 3. Review round (parallel)
Board: `stage: "review"`, increment `round`, reset all four `reviews` to
`"pending"`. Create `factory/jobs/<id>/round-<n>/` and spawn all four reviewers
**in parallel**, each pointed at the spec, the branch diff, and its own output
file in the round folder:

| agent           | model  | writes                |
|-----------------|--------|-----------------------|
| review-security | opus   | review-security.md    |
| review-ux       | sonnet | review-ux.md          |
| review-ui       | sonnet | review-ui.md          |
| review-code     | sonnet | review-code.md        |

As each verdict file lands, update `reviews` on the board (`PASS` / `CHANGES`).

**WAIT FOR ALL:** the round is done only when all four files exist in the round
folder. Never resume the builder mid-round.

### 4. Route
- **Any CHANGES** → board: `stage: "build"` (leave the failed verdicts visible),
  then resume `builder-<id>` with SendMessage, pointing it at the round folder
  (`round-<n>/`). It fixes, commits, appends to `build.md`. Then go back to
  step 3 for a new round. **Max 2 rounds**: if round 2 still has CHANGES, skip
  to the approver anyway — it will likely escalate.
- **All PASS** → approver.

### 5. approver (opus)
Board: `stage: "approval"`. Spawn the `approver` agent pointed at the job
folder. It writes `factory/jobs/<id>/decision.md` starting with `APPROVE` or
`ESCALATE`.
- `APPROVE` → merge `factory/<id>` into main, board `stage: "merged"`.
- `ESCALATE` → board `stage: "needs-human"`. A human runs `/factory approve`
  or `/factory rework`.

## Rules

- Agents get context from **files, not the conversation**. Give each agent the
  exact paths to read and the one path it writes.
- Every review file starts with `VERDICT: PASS` or `VERDICT: CHANGES`.
- `decision.md` starts with `APPROVE` or `ESCALATE`.
- Only you write `board.json`. Keep it valid JSON at all times.

## board.json shape

```json
{
  "jobs": [
    {
      "id": "003-rate-limiting",
      "title": "Rate limiting",
      "branch": "factory/003-rate-limiting",
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

Stages: `spec` → `build` → `review` → `approval` → `merged`, or `needs-human`.
