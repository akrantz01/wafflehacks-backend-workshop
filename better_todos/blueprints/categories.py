from flask import Blueprint, jsonify, request

from ..authentication import login_required
from ..database import Category, db
from ..schema.categories import schema, update_schema
from ..schema.todo import multiple

categories = Blueprint("categories", __name__)


@categories.get("")
@login_required
def get_all():
    records = Category.query.all()
    return jsonify(schema.from_objects(records))


@categories.post("")
@login_required
def create():
    body = schema.load(request.json)

    # Persist the category
    category = Category(**body)
    db.session.add(category)
    db.session.commit()

    return "", 201


@categories.put("/<int:cid>")
@login_required
def update(cid: int):
    body = update_schema.load(request.json)
    category = Category.query.get(cid)

    # Change anything if needed
    if body.get("name"):
        category.name = body.get("name")

    # Handle nullable fields
    try:
        category.description = body["description"]
    except KeyError:
        pass

    # Persist the updates
    db.session.commit()

    return "", 204


@categories.delete("/<int:cid>")
@login_required
def delete(cid: int):
    category = Category.query.get(cid)
    db.session.delete(category)
    db.session.commit()

    return "", 204


@categories.get("/<int:cid>/todos")
@login_required
def get_todos(cid: int):
    category = Category.query.get(cid)
    return jsonify(multiple.from_objects(category.todos))
