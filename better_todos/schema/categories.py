from marshmallow.fields import Integer, String
from marshmallow.validate import Length

from .base import Base


class Category(Base):
    id = Integer(required=True, dump_only=True)
    title = String(required=True, validate=Length(min=1, max=64))
    description = String()


# Derived schemas
schema = Category()
update = Category(partial=True)
