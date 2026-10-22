# SPDX-License-Identifier: MIT

import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class BaseConfig:
    """Application configuration class."""

    # Flask config
    SECRET_KEY = os.getenv("SECRET_KEY")
    FLASK_LOG_FILE = os.getenv("FLASK_LOG_FILE")

    # Elasticsearch config
    ELASTIC_URL = os.getenv("ELASTIC_URL")
    ELASTIC_USERNAME = os.getenv("ELASTIC_USERNAME")
    ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")
    INDEX_NAME = os.getenv("INDEX_NAME")

    # Pagination
    POSTS_PER_PAGE = os.getenv("POSTS_PER_PAGE")
