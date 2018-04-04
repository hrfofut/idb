from flask import Flask, render_template
from flask_assets import Environment, Bundle

import logging
from logging.handlers import RotatingFileHandler


# We can probably edit the file structure to make things easier

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .views.general import general
from .views.foods import foods
from .views.gyms import gyms
from .views.stores import stores
from .views.workouts import workouts
from .views.api import api


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('default_config.py')
    app.config.from_pyfile('application.py', silent=True)

    # Convert scss files to css
    assets = Environment(app)
    assets.url = app.static_url_path
    scss = Bundle('style.scss', filters='pyscss', output='style.css')
    assets.register('scss_all', scss)

    # Blueprints
    app.register_blueprint(general)
    app.register_blueprint(foods, url_prefix='/foods')
    app.register_blueprint(gyms, url_prefix='/gyms')
    app.register_blueprint(stores, url_prefix='/stores')
    app.register_blueprint(workouts, url_prefix='/workouts')
    app.register_blueprint(api, subdomain='api')

    #
    DB_URL = app.config['DB_URI']
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    #
    import idb.views

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(e):
        return render_template('errors/500.html'), 500

    return app


app = create_app(__name__)

formatter = logging.Formatter(
    "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")

handler = RotatingFileHandler(app.config.get('LOG_FILENAME',
                                             'idb.log'),
                              maxBytes=10000000,
                              backupCount=5)

handler.setFormatter(formatter)
app.logger.addHandler(handler)

mode = app.config.get('MODE', 'DEV')

if mode == 'PRODUCTION':
    app.logger.setLevel(app.config.get('LOG_LEVEL', logging.WARNING))
    assert app.config['SERVER_NAME']
    # app.run()
elif mode == 'DEV':
    app.logger.setLevel(app.config.get('LOG_LEVEL', logging.DEBUG))
    # app.run(host='0.0.0.0', port=5000)
