import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# ------------ Owen Lib ------------- #
from TODOApp import models
from TODOApp import tasks


def create_app(config_name):
    # App config
    app = Flask(__name__)
    app.config.from_object(config_name)

    # DataBase
    db = SQLAlchemy()

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # DataBase config
    db.init_app(app)

    # Views of project
    app.register_blueprint(tasks.bp)

