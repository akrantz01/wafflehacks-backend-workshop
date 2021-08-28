from typing import NewType
from marshmallow.fields import AwareDateTime, Boolean, Integer, List, Nested, String
from marshmallow.validate import Length

from .base import Base
from .categories import Category
from .tags import Tag


class Todo(Base):
    id = Integer(required=True, dump_only=True)
    title = String(required=True, validate=Length(min=1, max=128))
    content = String(required=False)
    complete = Boolean(load_default=False)
    due = AwareDateTime(format="iso")
    created_at = AwareDateTime(format="iso", dump_only=True)
    last_updated = AwareDateTime(format="iso", dump_only=True)
    category = Nested(Category, required=True, dump_only=True)
    tags = Nested(Tag, required=True, dump_only=True)


class TodoModify(Base):
    title = String(required=True, validate=Length(min=1, max=128))
    content = String(required=False)
    complete = Boolean(load_default=False)
    due = AwareDateTime(format="iso")
    category = Integer(required=False)
    tags = List(Integer, required=True)


# Derived schema
create = TodoModify()
update = TodoModify(partial=True)
single = Todo()
multiple = Todo(partial=("id", "title", "complete", "category", "tags", "due"))
