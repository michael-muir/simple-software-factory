VERDICT: PASS

Checked by running the CLI in the worktree.

- `python greet.py` prints `Hello, world!` and exits 0.
- `--help` shows usage with the description "Print a friendly greeting." and exits 0.
- `--bogus` prints `greet.py: error: unrecognized arguments: --bogus` to stderr and exits 2. The error is plain and standard.
- The happy path is obvious. There are no options beyond `-h`, which matches the spec.
- The docstrings are short and clear. The test names describe what they check.

No changes requested.
