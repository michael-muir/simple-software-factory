# Repo notes (written by the orchestrator)

## State

There is **no application code yet**. The repo holds only the factory itself
(`.claude/`, `factory/`, `README.md`, `BUILD_PROMPT.md`). Don't modify any of
those; they are not part of the product.

Several jobs run in parallel from the same `main`, so the conventions below are
fixed here up front. Follow them exactly so branches merge cleanly.

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

## Tests

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
