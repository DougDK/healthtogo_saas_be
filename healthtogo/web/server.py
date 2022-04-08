from flask import Flask, request
from flask_cors import CORS
from flask import jsonify

import healthtogo.core.app as core_app
from healthtogo.api.api import register as register_api
from healthtogo.core.types import H2GApp


def create_app(config=None) -> H2GApp:
    """Creates the API web server application from the shared Flask base app. Adds CORS,
       API REST methods, and the root health check method"""

    app = core_app.create_base_app(name="healthtogo", override_config=config)

    CORS(app)
    register_api(app)

    @app.route("/", methods=["GET"])
    @app.route("/healthz", methods=["GET"])
    def health():  # noqa: W0612 # pylint: disable=unused-variable
        return jsonify({"Status": "OK"})

    return app
