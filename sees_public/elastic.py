# SPDX-License-Identifier: MIT

from elasticsearch import Elasticsearch
from flask import Flask, current_app


def init_elastic(app: Flask) -> None:
    """Creates the elastic search client and registers it on the Flask app."""
    app.extensions["elastic"] = Elasticsearch(
        [app.config["ELASTIC_URL"]],
        basic_auth=(app.config["ELASTIC_USERNAME"], app.config["ELASTIC_PASSWORD"]),
        verify_certs=False,
    )


def get_elastic() -> Elasticsearch:
    """Return the current app elastic search client."""
    return current_app.extensions["elastic"]
