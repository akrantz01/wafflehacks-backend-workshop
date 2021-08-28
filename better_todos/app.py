from flask import Flask
from werkzeug.exceptions import HTTPException

from . import blueprints, database


# Configure the app
app = Flask(__name__)
app.config.from_object("better_todos.config")

# Setup dependencies
database.init(app)


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
