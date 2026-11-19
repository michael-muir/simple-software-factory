"""Tests for the greet command-line script."""

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


class GreetingTest(unittest.TestCase):
    """Tests for greet.greeting()."""

    def test_greeting_returns_hello_world(self) -> None:
        """greeting() returns the default greeting text."""
        self.assertEqual(greet.greeting(), "Hello, world!")

    def test_greeting_uses_name(self) -> None:
        """greeting(name) greets that name."""
        self.assertEqual(greet.greeting("Ada"), "Hello, Ada!")


class ParseNameTest(unittest.TestCase):
    """Tests for greet.parse_name()."""

    def test_strips_surrounding_whitespace(self) -> None:
        """Leading and trailing whitespace goes; inner spaces stay."""
        self.assertEqual(greet.parse_name("  Ada Lovelace\t "), "Ada Lovelace")

    def test_rejects_blank(self) -> None:
        """Empty and whitespace-only names raise ArgumentTypeError."""
        for value in ["", "   ", "\t", " \t\n "]:
            with self.subTest(value=value):
                with self.assertRaises(argparse.ArgumentTypeError):
                    greet.parse_name(value)


class MainTest(unittest.TestCase):
    """Tests for greet.main()."""

    def test_main_prints_default_greeting(self) -> None:
        """main([]) prints the greeting on one line and returns 0."""
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            result = greet.main([])
        self.assertEqual(result, 0)
        self.assertEqual(buffer.getvalue(), "Hello, world!\n")

    def test_name_separate_argument(self) -> None:
        """main(["--name", "Ada"]) greets Ada and returns 0."""
        code, out, err = run_main(["--name", "Ada"])
        self.assertEqual(code, 0)
        self.assertEqual(out, "Hello, Ada!\n")
        self.assertEqual(err, "")

    def test_name_equals_form(self) -> None:
        """main(["--name=Ada"]) greets Ada and returns 0."""
        code, out, err = run_main(["--name=Ada"])
        self.assertEqual(code, 0)
        self.assertEqual(out, "Hello, Ada!\n")
        self.assertEqual(err, "")

    def test_name_whitespace_is_normalised(self) -> None:
        """Surrounding whitespace is stripped from the name."""
        code, out, err = run_main(["--name", "  Ada Lovelace\t "])
        self.assertEqual(code, 0)
        self.assertEqual(out, "Hello, Ada Lovelace!\n")
        self.assertEqual(err, "")

    def test_blank_name_is_usage_error(self) -> None:
        """A blank name exits 2 with an error that mentions --name."""
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
        """--name with no value exits 2."""
        code, out, err = run_main(["--name"])
        self.assertEqual(code, 2)
        self.assertEqual(out, "")
        self.assertIn("--name", err)

    def test_help_mentions_name(self) -> None:
        """--help exits 0 and describes --name."""
        code, out, _ = run_main(["--help"])
        self.assertEqual(code, 0)
        self.assertIn("--name", out)
        self.assertIn("name to greet", out)


if __name__ == "__main__":
    unittest.main()
