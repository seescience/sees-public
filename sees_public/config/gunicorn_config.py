# SPDX-License-Identifier: MIT

import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration options
bind = os.getenv("GUNICORN_BIND", "0.0.0.0:5001")
workers = int(os.getenv("GUNICORN_WORKERS", "4"))
timeout = int(os.getenv("GUNICORN_TIMEOUT", "60"))
graceful_timeout = int(os.getenv("GUNICORN_GRACEFUL_TIMEOUT", "30"))
accesslog = os.getenv("GUNICORN_ACCESS_LOG")
errorlog = os.getenv("GUNICORN_ERROR_LOG")

# Create directories for log files if needed
if accesslog:
    Path(accesslog).parent.mkdir(parents=True, exist_ok=True)
if errorlog:
    Path(errorlog).parent.mkdir(parents=True, exist_ok=True)
