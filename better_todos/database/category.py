from .engine import db


class Categoy(db.Model):
    """
    The representation of a category in the database

    One category has many todos
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text, nullable=True)

