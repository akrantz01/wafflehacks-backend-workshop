from .engine import db


class Tag(db.Model):
    """
    The representation of a tag in the database

    One tag has many todos
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nulllable=False)
    color = db.Column(db.String(6), nullable=False)
