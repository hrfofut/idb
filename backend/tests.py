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

# import flaskr


from io import StringIO
from unittest import main, TestCase

from idb import create_app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import exists, update, and_
from idb.views.general import splash, search, about
from idb.views.foods import overview, detail, create_item
from idb.views.gyms import overview, detail, create_item
from idb.views.stores import overview, detail, create_item
from idb.views.workouts import overview, detail, create_item
# -------
# TestWeb
# -------


class FlaskrTestCase (TestCase):

    def setUp(self):
        # self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        # app = Flask(__name__, instance_relative_config=True)
        app = create_app("__test__")
        app.testing = True
        app.config.from_pyfile('default_config.py')
        app.config.from_pyfile('application.py', silent=True)

        app.config['SQLALCHEMY_DATABASE_URI'] = app.config['DB_URI']
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app = app.test_client()
        # with flaskr.app.app_context():
        #     flaskr.init_db()

    # def tearDown(self):
        # os.close(self.db_fd)
        # os.unlink(flaskr.app.config['DATABASE'])

    def test_test(self):
        self.assertEqual(1, 1)

    def test_general_splash(self):
        assert(self.app.get('/') is not None)  # splash

    def test_general_search(self):
        # print("App info:"+str(type(self.app)))
        result = self.app.post('/search', data={'search': 'bacon'})
        assert (result is not None)

    def test_general_about(self):
        assert (self.app.get('/about') is not None)

# ----
# main
# ----


if __name__ == "__main__":  # pragma: no cover
    main()
