VERDICT: PASS

Security review of `factory/001-hello-world-cli` (commit e546581), round 1.

Scope checked: `greet.py` and `tests/test_greet.py`, which are the only files
changed (`git diff --stat main...HEAD`).

Findings: none blocking.

- Injection / unsafe input: there is none. The only input is argv, and it goes
  to `argparse` with no options except the built-in `-h/--help`. Unknown
  arguments are rejected with exit code 2 (checked with `--bogus`). Nothing
  from the user is formatted into output, run by a shell, passed to
  `eval`/`exec`, or used as a file path.
- Path traversal / filesystem: the code reads and writes no files.
- Secrets: no credentials, tokens, keys, or environment-variable reads.
- Authn/authz: not applicable. It is a local CLI that needs no privileges.
- Dependencies: standard library only (`argparse`, `sys`, `contextlib`, `io`,
  `unittest`). No third-party packages and no new manifest files.
- Import side effects: `import greet` does nothing beyond defining things. The
  `__main__` guard is present, so importing runs no code.
- Tests: no subprocesses. They call `greet.main([])` with an explicit empty
  list, so the test runner's argv is never parsed.

Verified: `python greet.py` prints `Hello, world!` and exits 0; `--bogus` exits 2
with the usage error on stderr; `python -m unittest discover -s tests -v` ran
2 tests and both passed.

Note for job 002: when `--name` is added, the user-supplied value will be
printed to the terminal. That is fine for plain output. Don't pass it to a shell,
a file path, or a format string used as a template.
