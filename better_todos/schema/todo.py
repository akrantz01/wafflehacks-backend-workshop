from typing import NewType
from marshmallow.fields import AwareDateTime, Boolean, Integer, List, Nested, String
from marshmallow.validate import Length

from .base import Base
from .categories import Category
from .tags import Tag


class Todo(Base):
    id = Integer(required=True)
    title = String(required=True, validate=Length(min=1, max=128))
    content = String(required=False)
    complete = Boolean(load_default=False)
    due = AwareDateTime(format="iso")
    created_at = AwareDateTime(format="iso")
    last_updated = AwareDateTime(format="iso")
    category = Nested(Category, required=True)
    tags = Nested(Tag, required=True, many=True)


class TodoModify(Base):
    title = String(required=True, validate=Length(min=1, max=128))
    content = String(required=False, allow_none=True)
    complete = Boolean(load_default=False)
    due = AwareDateTime(format="iso")
    category = Integer(required=False, allow_none=True)
    tags = List(Integer, required=True)


# Derived schema
create_schema = TodoModify()
update_schema = TodoModify(partial=True)
single = Todo()
multiple = Todo(only=("id", "title", "complete", "category", "tags", "due"))
