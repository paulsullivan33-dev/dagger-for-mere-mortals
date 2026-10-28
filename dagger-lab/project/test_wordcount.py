"""Tests for wordcount.py, using only Python's standard library
so the test run needs no packages installed."""

import unittest

from wordcount import count


class CountTests(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(count(""), (0, 0, 0))

    def test_one_line(self):
        self.assertEqual(count("hello world\n"), (1, 2, 12))

    def test_two_lines(self):
        self.assertEqual(count("one\ntwo three\n"), (2, 3, 14))


if __name__ == "__main__":
    unittest.main()
