#!/usr/bin/env python3

# pylint: disable = bad-whitespace
# pylint: disable = invalid-name
# pylint: disable = missing-docstring

# ---------------------
# backend website tests
# ---------------------

# https://docs.python.org/3.4/reference/simple_stmts.html#grammar-token-assert_stmt

# -------
# imports
# -------

from io import StringIO
from unittest import main, TestCase

# -------
# TestWeb
# -------


class TestWeb (TestCase):

    def test_test(self):
        self.assertEqual(1, 1)

# ----
# main
# ----


if __name__ == "__main__":  # pragma: no cover
    main()
