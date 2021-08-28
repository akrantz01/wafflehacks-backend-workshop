from flask import Flask
from werkzeug.exceptions import HTTPException


# Configure the app
app = Flask(__name__)
app.config.from_object("better_todos.config")

# Setup dependencies


# Register the blueprints (modules)


# Register any error handlers
@app.errorhandler(HTTPException)
def http_exception(error: HTTPException):
    """
    Convert HTTP exceptions into JSON
    :param error: the HTTP exception
    :returns: a JSON response with the desired status code
    """
    return {"code": error.code, "message": error.name.lower()}, error.code
