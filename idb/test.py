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
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import exists, update, and_
from .. import idb
from views.general import splash, search, about
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
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('default_config.py')
    app.config.from_pyfile('application.py', silent=True)

    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['DB_URI']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    print("DB created?")
    main()
