# SPDX-License-Identifier: MIT

import logging
import urllib3
from logging.handlers import RotatingFileHandler
from pathlib import Path

from flask import Flask
from gunicorn.app.base import BaseApplication

from sees_public.config import BaseConfig
from sees_public.elastic import init_elastic
from sees_public.routes import data_bp


class SEESApp(BaseApplication):
    """Creates the SEES public application."""

    def __init__(self, dev_mode=False, options=None) -> None:

        # gunicorn options
        self.options = options or {}

        super(SEESApp, self).__init__()

        # flask application
        self.application = Flask(__name__)
        self.application.config.from_object(BaseConfig)

        # check for required variables
        missing = [key for key in BaseConfig.REQUIRED if not self.application.config.get(key)]
        if missing:
            raise RuntimeError(f"Missing required settings: {', '.join(missing)}")

        # init elastic search client
        init_elastic(app=self.application)

        # configure logging
        if not dev_mode:
            self._setup_logging()

        # register routes
        self.application.register_blueprint(data_bp)

        # log startup info
        self.application.logger.info("SEES Public app started")

    def _setup_logging(self) -> None:
        """Sets up the logging for production."""
        # flask log file
        log_file = self.application.config["FLASK_LOG_FILE"]

        # create the flask log directory if needed
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        # setup the file handler
        file_handler = RotatingFileHandler(log_file, maxBytes=10240000, backupCount=10)
        file_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
        file_handler.setLevel(logging.INFO)

        # setup logger
        self.application.logger.addHandler(file_handler)
        self.application.logger.setLevel(logging.INFO)
        self.application.logger.info("SEES Public application startup")

    def load_config(self) -> None:
        for key, value in self.options.items():
            if value is not None and key in self.cfg.settings:
                self.cfg.set(key.lower(), value)

    def load(self):
        """Returns WSGI/ASGI application."""
        return self.application

    def run_dev(self, port: int) -> None:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.application.run(host="0.0.0.0", port=port, debug=True)
