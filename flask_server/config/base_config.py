#!/usr/bin/env python3
# ----------------------------------------------------------------------------------
# Project: SEES Public
# File: flask_server/config/base_config.py
# ----------------------------------------------------------------------------------
# Purpose:
# This file is used to define the configuration settings for the Flask application.
# ----------------------------------------------------------------------------------
# Author: Christofanis Skordas
#
# Copyright (C) 2025 GSECARS, The University of Chicago, USA
# Copyright (C) 2025 NSF SEES, USA
# ----------------------------------------------------------------------------------

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
