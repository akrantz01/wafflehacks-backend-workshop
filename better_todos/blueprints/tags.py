from operator import mul
from flask import Blueprint, jsonify, request
import random

from ..authentication import authentication
from ..database import Tag, db
from ..schema.tags import schema, update_schema
from ..schema.todo import multiple

DEFAULT_COLORS = ["ffb5e8", "b28dff", "85e3ff", "ffabab", "aff8db", "fff5ba"]

tags = Blueprint("tags", __name__)


@tags.get("")
@authentication.login_required
def get_all():
    records = Tag.query.all()
    return jsonify(schema.from_objects(records))


@tags.post("")
@authentication.login_required
def create():
    body = schema.load(request.json)

    # Generate a color if one wasn't provided
    if not body.get("color"):
        body["color"] = random.choice(DEFAULT_COLORS)

    # Persist the tag
    tag = Tag(**body)
    db.session.add(tag)
    db.session.commit()

    return "", 201


@tags.put("/<int:tid>")
@authentication.login_required
def update(tid: int):
    body = update_schema.load(request.json)
    tag = Tag.query.get(tid)

    # Change anything if needed
    if body.get("name"):
        tag.name = body.get("name")
    if body.get("color"):
        tag.color = body.get("color")

    # Persist the updates
    db.session.commit()

    return "", 204


@tags.delete("/<int:tid>")
@authentication.login_required
def delete(tid: int):
    tag = Tag.query.get(tid)
    db.session.delete(tag)
    db.session.commit()

    return "", 204


@tags.get("/<int:tid>/todos")
@authentication.login_required
def get_todos(tid: int):
    tag = Tag.query.get(tid)
    return jsonify(multiple.from_objects(tag.todos))
