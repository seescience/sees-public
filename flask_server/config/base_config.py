# SPDX-License-Identifier: MIT

import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class BaseConfig:
    """Application configuration class."""

    # Basic Flask config
    SECRET_KEY = os.getenv("SECRET_KEY")
    DEBUG = os.getenv("DEBUG").lower() == "true"
    TESTING = os.getenv("TESTING").lower() == "true"

    # Logging configurationz
    FLASK_LOG_FILE = os.getenv("FLASK_LOG_FILE")

    # Elasticsearch config
    ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL")
    INDEX_NAME = os.getenv("INDEX_NAME")

    # Pagination
    POSTS_PER_PAGE = os.getenv("POSTS_PER_PAGE")
