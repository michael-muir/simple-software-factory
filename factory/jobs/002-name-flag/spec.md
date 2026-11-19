# 002-name-flag: Add a `--name` flag to the greeting CLI

## Goal

Let users greet someone specific. The greeting CLI (`greet.py`, laid out as
described in `factory/repo.md`) prints `Hello, world!` by default. This job adds
an optional `--name NAME` flag so that it prints `Hello, NAME!` instead. Input is
normalised: surrounding whitespace is stripped, and an empty or blank name is
rejected as a usage error. It is not silently turned back into "world". The
default behaviour does not change, so existing users see the same output.

## Scope

**In**

- An optional `--name` argument, parsed with `argparse`. Both `--name Ada` and
  `--name=Ada` work.
- Stripping leading and trailing whitespace from the name (`str.strip()`).
  Whitespace inside the name is kept as is.
- Rejecting a name that is empty or whitespace-only with an argparse usage error
  (exit status 2).
- A `--help` description for the flag.
- Unit tests for all of the above in `tests/test_greet.py`.
- **The base CLI, if it is missing.** This branch starts from `main`, which may
  not have `greet.py` yet, because job 001 is building it in parallel. If
  `greet.py` is missing, the builder creates the minimal base CLI as `repo.md`
  describes it (default output exactly `Hello, world!` plus a newline, exit
  code 0) and adds the flag on top. If `greet.py` is present, for example after
  syncing with `main`, extend it: keep its existing structure, function names
  and tests, and don't add a second greeting function next to the existing one.

**Out**

- A positional name argument, a short `-n` alias, environment variables, or
  config files.
- Greeting several names, changing the greeting word, or i18n.
- Length limits, or escaping or sanitising control characters in the name. The
  name is the user's own input, printed to their own terminal.
- Names that start with `-` given in the separate-argument form
  (`--name -x`). argparse's default behaviour is fine there.
- Rate limiting. That is a separate backlog item.
- Any change to `.claude/`, `factory/`, `README.md` or `BUILD_PROMPT.md`.

## Acceptance criteria

1. **Default is unchanged.** `greet.main([])` writes exactly `Hello, world!\n`
   to stdout and returns `0`.
2. **Name is used.** `greet.main(["--name", "Ada"])` writes exactly
   `Hello, Ada!\n` to stdout and returns `0`. `greet.main(["--name=Ada"])` does
   the same.
3. **Whitespace is normalised.** `greet.main(["--name", "  Ada Lovelace\t "])`
   writes exactly `Hello, Ada Lovelace!\n` and returns `0`. Leading and trailing
   whitespace is stripped and the inner space is kept.
4. **Blank names are rejected.** For `--name ""`, `--name "   "` (spaces only)
   and `--name "\t"`, `greet.main([...])` raises `SystemExit` with code `2`,
   writes nothing to stdout, and writes an error message to stderr that contains
   `--name`. `greet.main(["--name"])` (flag with no value) also exits with
   code `2`.
5. **Help.** `greet.main(["--help"])` exits with code `0`, and its output
   mentions `--name` with a short description.
6. **Structure follows repo.md.** `greet.py` is at the repo root, has
   `main(argv=None) -> int` and `if __name__ == "__main__": sys.exit(main())`,
   and builds the greeting text in a small, type-hinted function with a
   docstring that tests call directly, for example `greeting("Ada") == "Hello, Ada!"`.
   `main()` only parses arguments and prints. Only the standard library is
   used.
7. **Works from the shell.** From the repo root, `python greet.py --name Ada`
   prints `Hello, Ada!` with exit status 0, and `python greet.py --name ""`
   exits with status 2.
8. **Tests pass.** `tests/test_greet.py` covers criteria 1 to 6. It calls
   `greet.main([...])` and captures output with
   `contextlib.redirect_stdout` / `redirect_stderr`, without subprocesses.
   `python -m unittest discover -s tests -v`, run from the repo or worktree
   root, reports no failures or errors. The only files changed are `greet.py`
   and `tests/` (plus `tests/__init__.py` if needed).
