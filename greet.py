"""A small command-line script that prints a greeting."""

import argparse
import sys


def greeting() -> str:
    """Return the default greeting."""
    return "Hello, world!"


def main(argv: list[str] | None = None) -> int:
    """Parse command-line arguments, print the greeting and return 0."""
    parser = argparse.ArgumentParser(description="Print a friendly greeting.")
    parser.parse_args(argv)
    print(greeting())
    return 0


if __name__ == "__main__":
    sys.exit(main())
