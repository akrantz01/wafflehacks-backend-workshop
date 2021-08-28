from datetime import datetime

from .engine import db
from .helpers import TimeStamp, tags_todos


class Todo(db.Model):
    """
    The representation of a todo in the database

    One todo has many tags
    """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False, unique=True)
    content = db.Column(db.Text)
    complete = db.Column(db.Boolean, default=False, nullable=False)
    due = db.Column(TimeStamp(timezone=True), nullable=True)
    created_at = db.Column(
        TimeStamp(timezone=True), nullable=False, default=datetime.now
    )
    last_updated = db.Column(TimeStamp(timezone=True), onupdate=datetime.now, default=datetime.now)

    # Many-to-one relationship with an optional category
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=True)
    category = db.relationship(
        "Category", lazy=True, backref=db.backref("todos", lazy=True)
    )

    # Many-to-many relationship with tags
    tags = db.relationship(
        "Tag", secondary=tags_todos, lazy="subquery", backref=db.backref("todos", lazy=True)
    )
