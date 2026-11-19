# Repo notes (written by the orchestrator)

## State

The product is `greet.py`, a small greeting CLI (default `Hello, world!`, plus a
`--name` flag), with tests in `tests/test_greet.py`. The factory itself
(`.claude/`, `factory/`, `README.md`, `BUILD_PROMPT.md`, `.gitignore`) is not
part of the product; feature work never modifies it.

Several jobs run in parallel from the same `main`, so the conventions below are
fixed here up front. Follow them exactly so branches merge cleanly.

## Setup

None. Python 3 standard library only; a fresh checkout or worktree needs
nothing installed.

## Dev server

None. The product is a command-line tool with no pages to serve. If a prompt
gives you a port, you won't need it unless a spec adds a web surface; check
behaviour by running the CLI, e.g. `python greet.py --name Ada`.

## Language and tooling

- **Python 3** standard library only. No third-party dependencies, no
  `requirements.txt`, no packaging (`pyproject.toml`) unless a spec asks.
- Run Python as `python` (3.15 on this machine). `python3` is a Windows Store
  alias here; don't use it.
- Platform: Windows 11; shell commands run in Git Bash. Use forward-slash paths.

## Layout

```
greet.py              # the greeting CLI (entry point, argparse, main())
tests/test_greet.py   # unittest tests for greet.py
```

- One module, `greet.py`, at the repo root, with a `main(argv=None) -> int`
  function and `if __name__ == "__main__": sys.exit(main())`.
- Keep logic in small functions that tests can call directly; `main()` only
  parses args and prints.

## Validation

```
python -m unittest discover -s tests -v
```

- Standard library `unittest` (pytest is not installed).
- Tests import `greet` from the repo root (the command above, run from the repo
  or worktree root, puts it on the path; add `tests/__init__.py` only if needed).
- Test the CLI by calling `greet.main([...])` and capturing stdout
  (`contextlib.redirect_stdout`), not by spawning subprocesses.

## Conventions

- PEP 8, 4-space indents, type hints on public functions, short docstrings.
- Commit messages: imperative, sentence case, no prefix, e.g.
  `Add hello-world greeting CLI`.
- Line endings: Git has `core.autocrlf=true`; just write normal files.
