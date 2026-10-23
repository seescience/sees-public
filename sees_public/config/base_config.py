# SPDX-License-Identifier: MIT

import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class BaseConfig:
    """Application configuration class."""

    # Flask config
    SECRET_KEY = os.getenv("SECRET_KEY")
    FLASK_LOG_FILE = os.getenv("FLASK_LOG_FILE")

    # Search config
    ELASTIC_URL = os.getenv("ELASTIC_URL")
    ELASTIC_USERNAME = os.getenv("ELASTIC_USERNAME")
    ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")
    INDEX_NAME = os.getenv("INDEX_NAME")
    PER_PAGE = int(os.getenv("PER_PAGE", "50"))

    # Data directory config
    DATA_DIR = Path(os.getenv("DATA_DIR", "/Volumes/public/data"))

    # Required configured variables
    REQUIRED = ["SECRET_KEY", "ELASTIC_URL", "ELASTIC_USERNAME", "ELASTIC_PASSWORD", "INDEX_NAME"]
