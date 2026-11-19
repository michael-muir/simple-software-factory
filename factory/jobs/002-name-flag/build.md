# Build notes: 002-name-flag

Branch `factory/002-name-flag`, worktree `.worktrees/002-name-flag`.
Commit `4bc724a` "Add --name flag to the greeting CLI".

## What changed

`greet.py` was not on `main`, so I created the base CLI as `repo.md` and job
001's spec describe it, then added the flag. Only two files were added:

- `greet.py` (repo root)
  - `greeting(name: str = DEFAULT_NAME) -> str` returns `"Hello, {name}!"`.
    Job 001's `greeting()` gets an optional parameter here; there is no second
    greeting function. `greeting()` still returns `"Hello, world!"`.
  - `parse_name(value: str) -> str` is the argparse `type=` for `--name`. It
    applies `str.strip()` and raises `argparse.ArgumentTypeError` if the
    result is empty, so argparse prints
    `error: argument --name: name must not be empty or blank` and exits 2.
  - `build_parser() -> argparse.ArgumentParser` has the description
    "Print a friendly greeting." and `--name NAME` (default `world`, help
    "name to greet (default: world)"). There is no `-n` alias and no
    positional argument.
  - `main(argv: list[str] | None = None) -> int` parses the arguments, prints
    `greeting(args.name)` and returns 0.
  - It ends with `if __name__ == "__main__": sys.exit(main())`. Standard
    library only. `import greet` prints nothing.
- `tests/test_greet.py` has 11 `unittest` tests. A helper `run_main(argv)`
  calls `greet.main(argv)` under `redirect_stdout` and `redirect_stderr`,
  catches `SystemExit`, and returns (code, stdout, stderr). No subprocesses
  are used. `tests/__init__.py` was not needed: `python -m` puts the cwd on
  `sys.path`.

Merge note for when 001 lands: both branches add `greet.py` and
`tests/test_greet.py`, so git will report add/add conflicts. The names and
structure match 001's spec (`greeting`, `main(argv)`, `greet.main([...])`
tests). The resolution should keep 001's file and add the `name` parameter,
`parse_name` and the `--name` argument on top, plus this branch's tests.

## How I tested

`python -m unittest discover -s tests -v` (from the worktree root): ran 11
tests, all OK.

Manual shell checks from the worktree root:

| Command | Output | Exit |
|---|---|---|
| `python greet.py` | `Hello, world!` (bytes `Hello, world!\r\n`) | 0 |
| `python greet.py --name Ada` | `Hello, Ada!` | 0 |
| `python greet.py --name=Ada` | `Hello, Ada!` | 0 |
| `python greet.py --name "  Ada Lovelace<TAB> "` | `Hello, Ada Lovelace!` | 0 |
| `python greet.py --name ""` | usage + `error: argument --name: name must not be empty or blank` | 2 |
| `python greet.py --name "   "` | same error | 2 |
| `python greet.py --name` | usage + `error: argument --name: expected one argument` | 2 |
| `python greet.py --help` | usage, description, `--name NAME  name to greet (default: world)` | 0 |
| `python greet.py --bogus` | usage + `unrecognized arguments: --bogus` | 2 |
| `python -c "import greet"` | (nothing) | 0 |

No line is longer than 79 characters. pycodestyle and pyflakes are not
installed, so I checked PEP 8 by hand.

## Acceptance criteria

1. **Default is unchanged.** PASS. `test_default_output`: `main([])` returns 0
   and prints exactly `"Hello, world!\n"` with empty stderr.
2. **Name is used.** PASS. `test_name_separate_argument` (`--name Ada`) and
   `test_name_equals_form` (`--name=Ada`) both print `"Hello, Ada!\n"` and
   return 0.
3. **Whitespace is normalised.** PASS.
   `test_name_whitespace_is_normalised` prints `"Hello, Ada Lovelace!\n"`;
   `ParseNameTests.test_strips_surrounding_whitespace` tests the helper
   directly.
4. **Blank names are rejected.** PASS. `test_blank_name_is_usage_error`
   checks `""`, `"   "`, `"\t"` and `--name=`. Each gives SystemExit code 2,
   empty stdout, and `--name` in stderr.
   `test_name_without_value_is_usage_error` covers bare `--name` (code 2,
   `--name` in stderr). `ParseNameTests.test_rejects_blank` tests the helper.
5. **Help.** PASS. `test_help_mentions_name`: exit code 0, and stdout
   contains `--name` and "name to greet".
6. **Structure follows repo.md.** PASS. `greet.py` is at the root and has
   `main(argv=None) -> int` and the `sys.exit(main())` guard. The text comes
   from the type-hinted, documented `greeting()`, which `GreetingTests`
   calls directly (`greeting("Ada") == "Hello, Ada!"`, `greeting() ==
   "Hello, world!"`). `main()` only parses and prints. Standard library only.
7. **Works from the shell.** PASS. See the table: `--name Ada` exits 0 and
   `--name ""` exits 2.
8. **Tests pass.** PASS. 11 tests, OK. They cover criteria 1 to 6 through
   `greet.main([...])` with `redirect_stdout`/`redirect_stderr` and no
   subprocesses. The commit touches only `greet.py` and
   `tests/test_greet.py`.

## Sync with main

I ran `git merge main` in the worktree. Main had moved to `f459d29`, which
merged job 001's `e546581` "Add hello-world greeting CLI". The merge commit
is `dcbd2f3` "Merge main into factory/002-name-flag", a real merge with no
rebase. As expected, `greet.py` and `tests/test_greet.py` had add/add
conflicts.

### How I resolved them

I kept job 001's structure, names and tests and added this branch's changes
on top, as the spec and `decision.md` say.

- `greet.py`
  - I kept 001's module docstring, and its `main()` still builds the
    `ArgumentParser` itself, with the same description and docstring.
    `build_parser()` is gone and `--name` is now added inside `main()`.
    `main()` still only parses and prints.
  - The existing `greeting()` gained the optional `name: str = DEFAULT_NAME`
    parameter. There is no second greeting function, and `greeting()` still
    returns `"Hello, world!"`.
  - I added `parse_name()` and the `--name` argument without changing them.
- `tests/test_greet.py`
  - I kept 001's module docstring, `GreetingTest` and `MainTest`, including
    001's `test_greeting_returns_hello_world` and
    `test_main_prints_default_greeting`.
  - I dropped my `test_default_greeting` and `test_default_output` because
    they duplicated 001's tests.
  - I added `test_greeting_uses_name` to `GreetingTest` and my six `--name`
    tests to `MainTest`. I also added a new `ParseNameTest` class (renamed
    from `ParseNameTests` to match 001's singular naming) and the
    `run_main()` helper. Every test method has a docstring, as in 001's
    tests.

`git diff --stat main HEAD` shows only `greet.py` (+26 −5) and
`tests/test_greet.py` (+86). Nothing under `factory/` was committed.

### Tests after the sync

`python -m unittest discover -s tests -v` ran 11 tests, all OK: 2 from
`GreetingTest`, 2 from `ParseNameTest` and 7 from `MainTest`. No conflict
markers are left, and no line is over 79 characters.

I re-ran the shell checks from the worktree root:

- `python greet.py` prints `Hello, world!` with empty stderr and exits 0.
- `--name Ada` and `--name=Ada` print `Hello, Ada!` and exit 0.
- A padded name prints `Hello, Ada Lovelace!` and exits 0.
- `--name ""` exits 2 with `argument --name: name must not be empty or blank`.
- Bare `--name` exits 2.
- `--help` exits 0 and shows `--name NAME  name to greet (default: world)`.
- `--bogus` exits 2.
- `import greet` prints nothing.

### Criteria re-check (002 spec)

1. Default unchanged: PASS (`MainTest.test_main_prints_default_greeting`).
2. Name is used: PASS (`test_name_separate_argument`,
   `test_name_equals_form`).
3. Whitespace normalised: PASS (`test_name_whitespace_is_normalised`,
   `ParseNameTest.test_strips_surrounding_whitespace`).
4. Blank names rejected: PASS (`test_blank_name_is_usage_error`,
   `test_name_without_value_is_usage_error`,
   `ParseNameTest.test_rejects_blank`).
5. Help: PASS (`test_help_mentions_name`).
6. Structure: PASS. It now follows 001's layout. `greeting()` is extended
   rather than duplicated, `main(argv=None) -> int` only parses and prints,
   and the `sys.exit(main())` guard and standard-library-only imports are
   unchanged.
7. Shell: PASS (see the checks above).
8. Tests pass: PASS. 11 tests, OK. Relative to main, the branch changes only
   `greet.py` and `tests/test_greet.py`.

Job 001's own criteria still hold on the merged code: `greeting()` returns
`"Hello, world!"`, `main([])` prints `"Hello, world!\n"` and returns 0,
`--bogus` exits 2, and 001's tests pass unchanged. 001's criterion 5 ("`-h`
is the only option") is superseded by this job's `--name` flag, as intended.
