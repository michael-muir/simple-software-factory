"""A small command-line script that prints a greeting."""

import argparse
import sys

DEFAULT_NAME = "world"


def greeting(name: str = DEFAULT_NAME) -> str:
    """Return the greeting for ``name``; the default is ``"Hello, world!"``."""
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


def main(argv: list[str] | None = None) -> int:
    """Parse command-line arguments, print the greeting and return 0."""
    parser = argparse.ArgumentParser(description="Print a friendly greeting.")
    parser.add_argument(
        "--name",
        type=parse_name,
        default=DEFAULT_NAME,
        metavar="NAME",
        help="name to greet (default: %(default)s)",
    )
    args = parser.parse_args(argv)
    print(greeting(args.name))
    return 0


if __name__ == "__main__":
    sys.exit(main())
