VERDICT: PASS

Findings (round 1):
- Criteria 1-8 are met. I ran `python -m unittest discover -s tests -v` in the worktree: 11 tests, all OK.
- Shell checks pass. `python greet.py --name Ada` prints `Hello, Ada!`. `python greet.py --name ""` exits 2, and the stderr message names `--name`.
- Only `greet.py` and `tests/test_greet.py` changed. The code is standard library only, follows the repo.md layout, has type hints and docstrings, and `main()` only parses and prints.
- Tests cover default output, both name forms, whitespace stripping, blank names (including `--name=`), a missing value, and help. They use `redirect_stdout` and `redirect_stderr`, with no subprocesses.
- No dead code or duplication. Error handling goes through `argparse.ArgumentTypeError`, which gives exit 2.
- Nits, not blocking:
  - The `main(argv: list[str] | None)` annotation needs Python 3.10 or later. That is fine on 3.15.
  - Nothing tests that `main()` returns 0 for `--help`, because it raises `SystemExit`. The `--help` test covers that case.
