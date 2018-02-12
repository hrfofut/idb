from flask import Flask, render_template
import json
import requests
import logging
from logging.handlers import RotatingFileHandler

idb = Flask(__name__, instance_relative_config=True)
idb.config.from_pyfile('default_config.py')
idb.config.from_pyfile('idblication.py', silent=True)


@idb.route("/")
def splash(name=None):
    return render_template('splash.html')


@idb.route("/about")
def about():
    return render_template('about.html')


@idb.route("/foods")
def food():
    return render_template('foods/food.html')


@idb.route("/foods/<id>")
def fooddetail(id):
    """TODO: Have the template be filled from a database in the future"""
    return render_template('foods/fooddetail.html')


@idb.route("/workouts")
def workouts():
    return render_template('workouts/workouts.html')


@idb.route("/workouts/<id>")
def workoutsdetail(id):
    """TODO: Have the template be filled from a database in the future"""
    return render_template('workouts/workoutsdetail.html')


@idb.route("/gyms")
def gyms():
    return render_template('gyms/gyms.html')


@idb.route("/gyms/<id>")
def gymsdetail(id):
    """TODO: Have the template be filled from a database in the future"""
    return render_template('gyms/gymsdetail.html')


@idb.route("/stores")
def stores():
    return render_template('stores/stores.html')


@idb.route("/stores/<id>")
def storesdetail(id):
    """TODO: Have the template be filled from a database in the future"""
    return render_template('stores/storesdetail.html')

# Error handling


@idb.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@idb.errorhandler(500)
def internal_error(e):
    return render_template('errors/500.html'), 500


if __name__ == "__main__":
    formatter = logging.Formatter(
        "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
    handler = RotatingFileHandler(idb.config.get('LOG_FILENAME',
                                                 'idb.log'),
                                  maxBytes=10000000,
                                  backupCount=5)
    handler.setFormatter(formatter)
    idb.logger.addHandler(handler)
    idb.logger.setLevel(idb.config.get('LOG_LEVEL', logging.INFO))

    idb.run(host='0.0.0.0', port=4000)
