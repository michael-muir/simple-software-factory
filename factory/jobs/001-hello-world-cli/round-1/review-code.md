VERDICT: PASS

Checked against all 8 acceptance criteria.

- Files: the diff adds only greet.py and tests/test_greet.py. Both use only the standard library, and no tests/__init__.py is needed.
- CLI: `python greet.py` prints `Hello, world!` and exits 0. `--help` shows the description and exits 0. `--bogus` prints a usage error to stderr and exits 2.
- Structure: `greeting()` and `main(argv)` are typed and have docstrings. The module has a docstring and the `sys.exit(main())` guard. Importing prints nothing.
- Tests: `python -m unittest discover -s tests -v` ran 2 tests and both passed. The main test uses `main([])` with `redirect_stdout` and asserts the return value 0 and the output `"Hello, world!\n"`. No subprocesses are used.
- Commit message is `Add hello-world greeting CLI`.

No dead code, duplication or error-handling problems. No changes requested.
