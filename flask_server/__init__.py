#!/usr/bin/env python3
# ----------------------------------------------------------------------------------
# Project: SEES Public
# File: flask_server/__init__.py
# ----------------------------------------------------------------------------------
# Purpose:
# This is the main entry point for the application. This file is used to configure
# the Flask application.
# ----------------------------------------------------------------------------------
# Author: Christofanis Skordas
#
# Copyright (C) 2025 GSECARS, The University of Chicago, USA
# Copyright (C) 2025 NSF SEES, USA
# ----------------------------------------------------------------------------------

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from flask import Flask

from flask_server.config import BaseConfig

__all__ = ["create_flask_app"]


def create_flask_app() -> Flask:
    """Create and configure Flask application."""
    # Create the Flask app
    app = Flask(__name__)
    app.config.from_object(BaseConfig)

    # Setup logging
    if not app.debug and not app.testing:
        # Create directory for Flask log file if needed
        flask_log_path = Path(app.config["FLASK_LOG_FILE"])
        flask_log_path.parent.mkdir(parents=True, exist_ok=True)

        # Setup file handler
        file_handler = RotatingFileHandler(app.config["FLASK_LOG_FILE"], maxBytes=10240000, backupCount=10)
        file_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info("SEES Public application startup")

    # Import and register the routes
    from flask_server.routes import data_bp

    app.register_blueprint(data_bp)

    # Log startup info
    app.logger.info("SEES Public app started")

    return app
