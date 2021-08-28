from flask import Flask
from flask_cors import CORS


def init(app: Flask):
    # Define the origins that are allowed to make requests to your service
    if app.env == "development":
        # Localhost development (React, Vue, etc)
        origins = ["http://localhost:3000", "http://127.0.0.1:3000"]
    else:
        # Production deployment (the actual URL your service will run on)
        preferred_scheme = app.config.get("PREFERRED_URL_SCHEME")
        server_name = app.config.get("SERVER_NAME")
        origins = [f"{preferred_scheme}://{server_name}"]

    CORS(
        app,
        origins=origins,
        supports_credentials=True,
    )
