from flask import Blueprint, render_template

general = Blueprint('general', __name__)


@general.route("/")
def splash(name=None):
    return render_template('splash.html')


@general.route("/about")
def about():
    return render_template('about.html')

# Error handling


@general.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@general.errorhandler(500)
def internal_error(e):
    return render_template('errors/500.html'), 500

