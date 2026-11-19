"""Tests for the greet command-line script."""

import contextlib
import io
import unittest

import greet


class GreetingTest(unittest.TestCase):
    """Tests for greet.greeting()."""

    def test_greeting_returns_hello_world(self) -> None:
        """greeting() returns the default greeting text."""
        self.assertEqual(greet.greeting(), "Hello, world!")


class MainTest(unittest.TestCase):
    """Tests for greet.main()."""

    def test_main_prints_default_greeting(self) -> None:
        """main([]) prints the greeting on one line and returns 0."""
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            result = greet.main([])
        self.assertEqual(result, 0)
        self.assertEqual(buffer.getvalue(), "Hello, world!\n")


if __name__ == "__main__":
    unittest.main()
