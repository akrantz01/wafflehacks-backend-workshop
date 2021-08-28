from marshmallow import validate
from marshmallow.fields import Integer, String
from marshmallow.validate import Length, Regexp

from .base import Base


class Tag(Base):
    id = Integer(required=True, dump_only=True)
    name = String(required=True, validate=Length(min=1, max=64))
    color = String(validate=Regexp(r"^[0-9a-f]{6}$"), allow_none=True)


# Derived schemas
schema = Tag()
update_schema = Tag(partial=True)
