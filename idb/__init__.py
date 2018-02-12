from flask import Flask

import logging
from logging.handlers import RotatingFileHandler

from .views.general import general
from .views.foods import foods
from .views.gyms import gyms
from .views.stores import stores
from .views.workouts import workouts

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('default_config.py')
app.config.from_pyfile('application.py', silent=True)

# Blueprints
app.register_blueprint(general)
app.register_blueprint(foods, url_prefix='/foods/')
app.register_blueprint(gyms, url_prefix='/gymss/')
app.register_blueprint(stores, url_prefix='/storess/')
app.register_blueprint(workouts, url_prefix='/workouts/')

import idb.views

if __name__ == "__main__":
    formatter = logging.Formatter(
        "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
    handler = RotatingFileHandler(views.config.get('LOG_FILENAME',
                                                 'views.log'),
                                  maxBytes=10000000,
                                  backupCount=5)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(views.config.get('LOG_LEVEL', logging.INFO))

    app.run(host='0.0.0.0', port=5000)
