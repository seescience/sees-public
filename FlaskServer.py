#!/usr/bin/env python3
# ----------------------------------------------------------------------------------
# Project: SEES Public
# File: FlaskServer.py
# ----------------------------------------------------------------------------------
# Purpose:
# This is the main entry point for the SEES Public flask server application. This
# file is used to create the Flask app and run the gunicorn server.
# ----------------------------------------------------------------------------------
# Author: Christofanis Skordas
#
# Copyright (C) 2025 GSECARS, The University of Chicago, USA
# Copyright (C) 2025 NSF SEES, USA
# ----------------------------------------------------------------------------------

import argparse
import subprocess

from flask_server import create_flask_app

app = create_flask_app()


def main() -> None:
    """Main entry point for the application."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="SEES Public App")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug")
    parser.add_argument("-p", "--port", type=int, help="Port to run the server on. Default port is 5000.")
    args = parser.parse_args()

    # Run the Flask app
    if args.debug:
        app.run(host="0.0.0.0", port=args.port if args.port else 5000, debug=True)
    else:
        subprocess.run(["gunicorn", "-c", "flask_server/config/gunicorn_config.py", "FlaskServer:app"], check=False)


if __name__ == "__main__":
    main()
