from datetime import datetime, timezone, tzinfo
import sqlalchemy
from sqlalchemy.types import TypeDecorator

from .engine import db

# Define a table that to be used for a many-to-many relationship between todos and tags.
# A helper table must be used for this type of relationship.
tags_todos = db.Table(
    "tags_todos",
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"), primary_key=True),
    db.Column("todo_id", db.Integer, db.ForeignKey("todo.id"), primary_key=True),
)


# From https://mike.depalatis.net/blog/sqlalchemy-timestamps.html
class TimeStamp(TypeDecorator):
    impl = sqlalchemy.DateTime
    cache_ok = True
    LOCAL_TIMEZONE = datetime.now().astimezone().tzinfo

    def process_bind_param(self, value, dialect):
        if value.tzinfo is None:
            value = value.astimezone(self.LOCAL_TIMEZONE)
        
        return value.astimezone(timezone.utc)
    
    def process_result_value(self, value, dialect):
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        
        return value.astimezone(timezone.utc)
