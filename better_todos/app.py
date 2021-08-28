from flask import Flask
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import HTTPException

from . import blueprints, cors, database, schema


# Configure the app
app = Flask(__name__)
app.config.from_object("better_todos.config")

# Setup dependencies
cors.init(app)
database.init(app)
schema.init(app)


# Register the blueprints (modules)
for prefix, blueprint in blueprints.mapping.items():
    app.register_blueprint(blueprint, url_prefix=prefix)


# Register any error handlers
@app.errorhandler(HTTPException)
def http_exception(error: HTTPException):
    """
    Convert HTTP exceptions into JSON
    :param error: the HTTP exception
    :returns: a JSON response with the desired status code
    """
    return {"code": error.code, "message": error.name.lower()}, error.code


@app.errorhandler(ValidationError)
def validation_exception(error: ValidationError):
    return {"code": 400, "message": f"invalid field {error.field_name}"}, 400


@app.errorhandler(IntegrityError)
def integrity_exception(_):
    # Ideally we would be able to give more information for this,
    # however, the error format is different for each database
    # type (SQLite3, PostgreSQL, MySQL, etc).
    return {"code": 409, "message": "value must be unique"}, 409
