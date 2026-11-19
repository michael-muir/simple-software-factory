"""Tests for the greeting CLI in greet.py."""

import argparse
import contextlib
import io
import unittest

import greet


def run_main(argv: list[str]) -> tuple[int | str | None, str, str]:
    """Call ``greet.main(argv)`` and return (exit code, stdout, stderr).

    A ``SystemExit`` raised by argparse is caught and its code returned.
    """
    stdout = io.StringIO()
    stderr = io.StringIO()
    with contextlib.redirect_stdout(stdout):
        with contextlib.redirect_stderr(stderr):
            try:
                code = greet.main(argv)
            except SystemExit as exc:
                code = exc.code
    return code, stdout.getvalue(), stderr.getvalue()


class GreetingTests(unittest.TestCase):
    """The greeting() helper builds the text."""

    def test_default_greeting(self) -> None:
        self.assertEqual(greet.greeting(), "Hello, world!")

    def test_named_greeting(self) -> None:
        self.assertEqual(greet.greeting("Ada"), "Hello, Ada!")


class ParseNameTests(unittest.TestCase):
    """The parse_name() helper normalises and validates names."""

    def test_strips_surrounding_whitespace(self) -> None:
        self.assertEqual(greet.parse_name("  Ada Lovelace\t "), "Ada Lovelace")

    def test_rejects_blank(self) -> None:
        for value in ["", "   ", "\t", " \t\n "]:
            with self.subTest(value=value):
                with self.assertRaises(argparse.ArgumentTypeError):
                    greet.parse_name(value)


class MainTests(unittest.TestCase):
    """greet.main() parses arguments and prints the greeting."""

    def test_default_output(self) -> None:
        code, out, err = run_main([])
        self.assertEqual(code, 0)
        self.assertEqual(out, "Hello, world!\n")
        self.assertEqual(err, "")

    def test_name_separate_argument(self) -> None:
        code, out, err = run_main(["--name", "Ada"])
        self.assertEqual(code, 0)
        self.assertEqual(out, "Hello, Ada!\n")
        self.assertEqual(err, "")

    def test_name_equals_form(self) -> None:
        code, out, err = run_main(["--name=Ada"])
        self.assertEqual(code, 0)
        self.assertEqual(out, "Hello, Ada!\n")
        self.assertEqual(err, "")

    def test_name_whitespace_is_normalised(self) -> None:
        code, out, err = run_main(["--name", "  Ada Lovelace\t "])
        self.assertEqual(code, 0)
        self.assertEqual(out, "Hello, Ada Lovelace!\n")
        self.assertEqual(err, "")

    def test_blank_name_is_usage_error(self) -> None:
        cases = [
            ["--name", ""],
            ["--name", "   "],
            ["--name", "\t"],
            ["--name="],
        ]
        for argv in cases:
            with self.subTest(argv=argv):
                code, out, err = run_main(argv)
                self.assertEqual(code, 2)
                self.assertEqual(out, "")
                self.assertIn("--name", err)

    def test_name_without_value_is_usage_error(self) -> None:
        code, out, err = run_main(["--name"])
        self.assertEqual(code, 2)
        self.assertEqual(out, "")
        self.assertIn("--name", err)

    def test_help_mentions_name(self) -> None:
        code, out, _ = run_main(["--help"])
        self.assertEqual(code, 0)
        self.assertIn("--name", out)
        self.assertIn("name to greet", out)


if __name__ == "__main__":
    unittest.main()
