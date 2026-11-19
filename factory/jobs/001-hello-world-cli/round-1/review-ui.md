VERDICT: PASS

Visual surface is terminal output only. Checked by running it:
- `python greet.py` prints one line, `Hello, world!`, with exit 0 and nothing on stderr.
- `--help` prints a usage line, the description "Print a friendly greeting." and the `-h, --help` option. It is clean and standard argparse, and exits 0.
- `--bogus` prints a usage error to stderr and exits 2.

There is no colour, no custom formatting and no markup. No findings.
