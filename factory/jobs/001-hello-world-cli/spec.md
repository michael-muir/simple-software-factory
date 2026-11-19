# Spec: 001-hello-world-cli

## Goal

Create the product's first code: a small Python command-line script, `greet.py`,
that prints `Hello, world!` and exits successfully, plus one unittest test for
it. The point is to set up the module structure described in
`factory/repo.md` (a `main(argv=None) -> int` entry point, argparse, logic in
small testable functions, stdlib `unittest` tests) so later jobs, starting with
002 (`--name` flag), have a known base to build on. Keep it minimal.

## Scope

**In scope**
- `greet.py` at the repo root containing:
  - a small public function `greeting() -> str` that returns `"Hello, world!"`;
  - `main(argv: list[str] | None = None) -> int`, which builds an
    `argparse.ArgumentParser` with a one-line description, parses `argv`
    (`None` means `sys.argv[1:]`, which is argparse's default), prints
    `greeting()` and returns `0`;
  - `if __name__ == "__main__": sys.exit(main())`.
- `tests/test_greet.py` with at least one `unittest` test for the default
  greeting (more small tests are fine).
- `tests/__init__.py` only if discovery needs it (see `repo.md`).

**Out of scope**
- Any option other than argparse's built-in `-h/--help`. In particular, no
  `--name` flag and no `name` parameter on `greeting()`: job 002 adds those.
- Rate limiting, config files, logging, colour, localisation.
- Third-party dependencies, `requirements.txt`, `pyproject.toml`, packaging,
  console-script entry points.
- Any change to the factory itself: `.claude/`, `factory/`, `README.md`,
  `BUILD_PROMPT.md`, `.gitignore`.

## Acceptance criteria

1. **Files.** The branch adds `greet.py` (repo root) and `tests/test_greet.py`,
   plus `tests/__init__.py` only if needed, and changes nothing else. Both
   files use only the Python standard library.
2. **CLI default output.** Running `python greet.py` from the repo/worktree
   root writes exactly one line, `Hello, world!`, to stdout (the line ending
   is whatever the platform uses), writes nothing to stderr, and exits with
   code 0.
3. **Structure.** `greet.py` defines `greeting() -> str`, which returns exactly
   `"Hello, world!"`, and `main(argv: list[str] | None = None) -> int`, which
   uses argparse and ends with the `if __name__ == "__main__":
   sys.exit(main())` guard. Running `import greet` prints nothing.
4. **`main` contract.** `greet.main([])` returns `0`, and with stdout captured
   in a `io.StringIO` the captured text is exactly `"Hello, world!\n"`.
5. **Help and no other flags.** `python greet.py --help` prints usage,
   including the parser's description, and exits 0. `-h/--help` is the only
   option. An unknown argument such as `python greet.py --bogus` makes
   argparse print a usage error to stderr and exit with code 2.
6. **Test.** `tests/test_greet.py` has at least one `unittest.TestCase` test
   that calls `greet.main([])` (an explicit empty list, not `main()`, so the
   test runner's own `sys.argv` is not parsed), captures stdout with
   `contextlib.redirect_stdout`, and asserts both the return value `0` and
   the output `"Hello, world!\n"`. No tests start a subprocess.
7. **Test run passes.** `python -m unittest discover -s tests -v`, run from
   the repo/worktree root, finds and runs at least one test, and every test
   passes.
8. **Conventions.** PEP 8 with 4-space indents, type hints and a short
   docstring on every public function, plus a module docstring in `greet.py`.
   The commit message is `Add hello-world greeting CLI`.
