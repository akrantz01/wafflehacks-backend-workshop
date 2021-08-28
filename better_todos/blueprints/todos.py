from better_todos.database import category
from flask import Blueprint, abort, jsonify, request
from typing import List

from ..authentication import authentication
from ..database import Category, Tag, Todo, db
from ..schema.todo import create_schema, multiple, single, update_schema

todos = Blueprint("todos", __name__)


def load_tags(ids: List[int]) -> List[Tag]:
    tags = []

    for tag_id in ids:
        tag = Tag.query.get(tag_id)
        if tag is None:
            abort(400)
        tags.append(tag)

    return tags


@todos.get("")
@authentication.login_required
def get_all():
    records = Todo.query.all()
    return jsonify(multiple.from_objects(records))


@todos.post("")
@authentication.login_required
def create():
    body = create_schema.load(request.json)

    # Resolve the tags (if provided)
    tags = []
    if body.get("tags"):
        tags = load_tags(body.pop("tags"))

    # Resolve the category (if provided)
    category = None
    if body.get("category"):
        category = Category.query.get(body.pop("category"))
        if category is None:
            abort(400)

    # Persist the todo
    todo = Todo(**body, category=category, tags=tags)
    db.session.add(todo)
    db.session.commit()

    return "", 201


@todos.get("/<int:tid>")
@authentication.login_required
def get(tid: int):
    todo = Todo.query.get(tid)
    if todo is None:
        abort(404)

    return single.from_object(todo)


@todos.put("/<int:tid>")
@authentication.login_required
def update(tid: int):
    body = update_schema.load(request.json)
    todo = Todo.query.get(tid)
    if todo is None:
        abort(404)

    # Change anything if needed
    if body.get("title"):
        todo.title = body.get("title")
    if body.get("complete") is not None:
        todo.complete = body.get("complete")
    if body.get("tags"):
        tags = load_tags(body.pop("tags"))
        todo.tags = tags

    # Handle nullable fields
    try:
        todo.content = body["content"]
    except KeyError:
        pass
    try:
        todo.due = body["due"]
    except KeyError:
        pass
    try:
        category_id = body["category"]
        if category_id is not None:
            c = Category.query.get(category_id)
            if c is None:
                abort(400)
            todo.category = c
        else:
            todo.category = None
    except KeyError:
        pass

    # Persist the updates
    db.session.commit()

    return "", 204


@todos.delete("/<int:tid>")
@authentication.login_required
def delete(tid: int):
    todo = Todo.query.get(tid)
    db.session.delete(todo)
    db.session.commit()

    return "", 204


@todos.post("/<int:tid>/toggle")
@authentication.login_required
def toggle(tid: int):
    todo = Todo.query.get(tid)
    if todo is None:
        abort(404)

    todo.complete = not todo.complete
    db.session.commit()

    return "", 204
