# simple-software-factory

A tiny, visual software factory built from one Claude Code skill, seven
subagents, and markdown files. Everything a viewer needs fits in a few minutes
of reading.

## How it works

Run `/factory <feature>` in Claude Code. That session becomes the
**orchestrator**: it runs the loop, spawns every agent, and is the only writer
of `factory/board.json`.

```
feature → spec-writer → builder → [security · ux · ui · code] reviews
            (opus)      (opus)      (wait for ALL four verdicts)
                           ▲                 │
                           └── any CHANGES ──┘  (max 2 rounds)
                                             │ all PASS
                                             ▼
                                         approver → merge, or needs-human
                                          (opus)      (/factory approve)
```

Agents get context from files, not the conversation, and each writes exactly
one file. Reviews start with `VERDICT: PASS` or `VERDICT: CHANGES`;
`decision.md` starts with `APPROVE` or `ESCALATE`. The builder works on a
`factory/<id>` branch and is resumed (never respawned) for each review round.

## Parallel jobs

Up to 3 jobs run at once. Each job gets its own git worktree at
`.worktrees/<id>` on branch `factory/<id>`, so builders never share a working
directory. The main checkout stays on `main` and holds the board and every
job's markdown files. Approved jobs pass through a **merge gate** one at a
time: the branch is synced with `main` (the builder resolves any conflicts and
re-runs tests), merged, and its worktree removed. Escalated jobs keep their
worktree for a human to inspect.

## Commands

- `/factory <feature>` — run a new job through the loop
- `/factory next [n]` — start the first `n` unchecked items in `factory/backlog.md`
- `/factory approve <id>` — merge a `needs-human` job into main
- `/factory rework <id> <feedback>` — send a job back to the builder

## Dashboard

```sh
cd factory
python3 -m http.server 8000   # Windows: py -m http.server 8000
# open http://localhost:8000/dashboard.html
```

Jobs appear as cards moving across stages, with reviewer chips filling in as
verdicts land. `needs-human` jobs are highlighted. Click a card to read its
spec, build notes, reviews, and decision.

## Layout

```
.claude/skills/factory/SKILL.md   the orchestrator's instructions
.claude/agents/*.md               one file per agent in the loop
factory/board.json                durable state, drives the dashboard
factory/dashboard.html            the visual board
factory/backlog.md                feature queue for /factory next
factory/jobs/<id>/                spec.md, build.md, round-N/, decision.md
.worktrees/<id>/                  a job's code, on factory/<id> (gitignored)
```

To change the factory, edit `SKILL.md` (the loop) or the agent files (the
workers).
