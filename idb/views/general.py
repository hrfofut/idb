from flask import Blueprint, render_template

import requests

general = Blueprint('general', __name__)


@general.route("/")
def splash(name=None):
    return render_template('splash.html')


@general.route("/about")
def about():
    r = requests.get('https://api.github.com/repos/hrfofut/idb/stats/contributors')
    return render_template('about.html', statistics=r.text)

# Error handling


@general.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@general.errorhandler(500)
def internal_error(e):
    return render_template('errors/500.html'), 500

