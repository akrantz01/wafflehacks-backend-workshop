from flask import Flask
from flask_httpauth import HTTPBasicAuth
from os import environ

USERNAME = environ.get("AUTHENTICATION_USERNAME")
PASSWORD = environ.get("AUTHENTICATION_PASSWORD")
MESSAGES = {401: "unauthorized", 403: "forbidden"}

authentication = HTTPBasicAuth()
login_required = authentication.login_required


@authentication.verify_password
def verify(username: str, password: str):
    """
    Check the username and password are valid
    :param username: the username to check
    :param password: the password associated with the username
    """
    username_valid = USERNAME == username
    password_valid = PASSWORD == password

    if username_valid and password_valid:
        return username


@authentication.error_handler
def error_handler(status: int):
    """
    Convert any errors to JSON
    :param status: the status code being returned
    """
    return {
        "code": status,
        "message": MESSAGES[status],
    }, status
