APPROVE

- All 8 acceptance criteria are met. The diff (`main...HEAD`, one commit
  `e546581 Add hello-world greeting CLI`) adds only `greet.py` and
  `tests/test_greet.py`, uses only the standard library, and touches nothing
  in `.claude/`, `factory/`, `README.md`, `BUILD_PROMPT.md` or `.gitignore`.
- Round 1: all four reviewers (code, security, ui, ux) returned PASS with no
  findings and no requested changes. They do not contradict each other or
  the build notes.
- I checked it again myself in the worktree. Tests: 2 ran, both passed.
  `python greet.py` wrote exactly `Hello, world!\r\n` to stdout, nothing to
  stderr, exit 0. `--help` showed the description and only `-h, --help`,
  exit 0. `--bogus` gave the usage error on stderr, exit 2. `import greet`
  printed nothing.
- Scope is tight. There is no `--name` flag and no `name` parameter, as the
  spec requires, which leaves job 002 its starting point. The branch is based
  on the current `main` (`1351811`) and the worktree is clean (no stray
  `__pycache__` or temp files).
- Nothing alarming. The security reviewer's note for job 002 (never pass
  `--name` to a shell, a file path or a format template) is advice for
  later, not a problem with this job.
