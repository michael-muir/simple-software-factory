# Build: 001-hello-world-cli

Branch: `factory/001-hello-world-cli`
Commit: `e546581 Add hello-world greeting CLI`

## What changed

- **`greet.py`** (new, repo root). Has a module docstring, `greeting() -> str`
  returning `"Hello, world!"`, and `main(argv: list[str] | None = None) -> int`.
  `main` builds an `argparse.ArgumentParser(description="Print a friendly
  greeting.")`, calls `parse_args(argv)`, prints `greeting()` and returns `0`.
  The file ends with the `if __name__ == "__main__": sys.exit(main())` guard.
  Imports are only `argparse` and `sys`.
- **`tests/test_greet.py`** (new). Has two `unittest.TestCase` tests:
  - `GreetingTest.test_greeting_returns_hello_world` checks that `greeting()`
    returns `"Hello, world!"`.
  - `MainTest.test_main_prints_default_greeting` calls `greet.main([])` under
    `contextlib.redirect_stdout(io.StringIO())` and asserts the return value
    is `0` and the output is `"Hello, world!\n"`.
- No `tests/__init__.py`: discovery finds and imports the tests without it.
- Nothing else changed. `git diff --stat main...HEAD` lists only the two files
  above.

## How I tested

Everything was run from the worktree root with Python 3.15.2.

- `python -m unittest discover -s tests -v`: ran 2 tests, both OK, exit 0.
- `python greet.py`: stdout was exactly the bytes `Hello, world!\r\n` (checked
  with `od -c`; CRLF is the Windows line ending), stderr was 0 bytes, exit 0.
- `python greet.py --help`: printed `usage: greet.py [-h]`, the description
  `Print a friendly greeting.`, and an options list containing only
  `-h, --help`. Exit 0. `-h` also exits 0.
- `python greet.py --bogus`: stdout was empty, stderr was `usage: greet.py [-h]`
  then `greet.py: error: unrecognized arguments: --bogus`, exit 2. A stray
  positional argument (`extra`) is rejected the same way, also exit 2.
- `python -c "import greet"`: no output, exit 0.
- `greet.main([])` with stdout captured in `io.StringIO`: returned `0` and
  captured `'Hello, world!\n'`.
- Style: pycodestyle and flake8 are not installed, so I checked by hand. Both
  files use 4-space indents, contain no tabs, and have no line over 78
  characters. Every public function, class and test method has a docstring
  and type hints.

## Acceptance criteria

1. **Files**: PASS. The branch adds only `greet.py` and `tests/test_greet.py`,
   with no `tests/__init__.py` because discovery works without it. Both files
   use only the standard library (`argparse`, `sys`, `contextlib`, `io`,
   `unittest`).
2. **CLI default output**: PASS. stdout is exactly one line,
   `Hello, world!` followed by the platform line ending. stderr is empty and
   the exit code is 0.
3. **Structure**: PASS. `greeting() -> str` returns exactly `"Hello, world!"`.
   `main(argv: list[str] | None = None) -> int` uses argparse, and the
   `sys.exit(main())` guard is the last thing in the file. `import greet`
   prints nothing.
4. **`main` contract**: PASS. `greet.main([])` returns `0`, and the captured
   stdout is exactly `"Hello, world!\n"`.
5. **Help and no other flags**: PASS. `--help` prints usage with the
   description and exits 0, and `-h/--help` is the only option. `--bogus`
   writes a usage error to stderr and exits 2.
6. **Test**: PASS. `MainTest.test_main_prints_default_greeting` calls
   `greet.main([])`, captures stdout with `contextlib.redirect_stdout`, and
   asserts both `0` and `"Hello, world!\n"`. No test starts a subprocess.
7. **Test run passes**: PASS. 2 tests found, 2 OK.
8. **Conventions**: PASS. The code follows PEP 8 with 4-space indents, has a
   module docstring, and gives every public function type hints and a
   docstring. The commit subject is `Add hello-world greeting CLI`, followed
   by the Co-Authored-By trailer the session asks for.

## Notes

- Git prints "LF will be replaced by CRLF" on commit. That is expected with
  `core.autocrlf=true`, as `repo.md` says.
- No `__pycache__` directories were created in the worktree, so there is
  nothing to ignore or clean up.
