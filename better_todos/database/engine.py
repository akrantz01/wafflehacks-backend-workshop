from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init(app: Flask):
    """
    Initialize the database and create the necessary schema. Optionally, drop the current database and re-create it.
    :param app: the Flask application to attach to
    """
    db.init_app(app=app)

    if app.config.get("RESET_DATABASE"):
        db.drop_all(app=app)
    db.create_all(app=app)
