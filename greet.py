"""A small command-line greeting.

Prints ``Hello, world!`` by default, or ``Hello, NAME!`` with ``--name NAME``.
"""

import argparse
import sys

DEFAULT_NAME = "world"


def greeting(name: str = DEFAULT_NAME) -> str:
    """Return the greeting for ``name``, e.g. ``"Hello, Ada!"``."""
    return f"Hello, {name}!"


def parse_name(value: str) -> str:
    """Strip surrounding whitespace from ``value`` and reject blank names.

    Raises ``argparse.ArgumentTypeError`` if nothing is left after stripping,
    so argparse reports a usage error and exits with status 2.
    """
    name = value.strip()
    if not name:
        raise argparse.ArgumentTypeError("name must not be empty or blank")
    return name


def build_parser() -> argparse.ArgumentParser:
    """Return the argument parser for the greeting CLI."""
    parser = argparse.ArgumentParser(description="Print a friendly greeting.")
    parser.add_argument(
        "--name",
        type=parse_name,
        default=DEFAULT_NAME,
        metavar="NAME",
        help="name to greet (default: %(default)s)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the CLI with ``argv`` (``None`` means ``sys.argv[1:]``)."""
    args = build_parser().parse_args(argv)
    print(greeting(args.name))
    return 0


if __name__ == "__main__":
    sys.exit(main())
