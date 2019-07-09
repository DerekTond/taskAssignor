import os
import sys
import logging

from flask import Flask
from taskassignor.settings import config
from taskassignor.models import db
from taskassignor.view import view_bp



def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    db.init_app(app)


def register_blueprints(app):
    app.register_blueprint(view_bp)



if __name__ == '__main__':
    create_app().run()

# from taskassignor import views, commands
