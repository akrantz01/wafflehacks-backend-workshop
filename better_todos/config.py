from os import environ

SECRET_KEY = environ.get("SECRET_KEY")
SERVER_NAME = environ.get("SERVER_NAME", "localhost:5000")
PREFERRED_URL_SCHEME = environ.get("PREFERRED_URL_SCHEME", "http")

SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")
SQLALCHEMY_TRACK_MODIFICATIONS = False
RESET_DATABASE = environ.get("RESET_DATABASE", "false").lower() == "true"
