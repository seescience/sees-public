#!/usr/bin/env python3
# ----------------------------------------------------------------------------------
# Project: SEES Public
# File: flask_server/routes.py
# ----------------------------------------------------------------------------------
# Purpose:
# This file contains all the Flask routes for serving dynamic data content.
# ----------------------------------------------------------------------------------
# Author: Christofanis Skordas
#
# Copyright (C) 2025 GSECARS, The University of Chicago, USA
# Copyright (C) 2025 NSF SEES, USA
# ----------------------------------------------------------------------------------

#!/usr/bin/env python3
from pathlib import Path

from flask import Blueprint, abort, render_template, send_from_directory

# Create blueprint for data routes
data_bp = Blueprint("data", __name__)


# Home route
@data_bp.route("/")
def home():
    """Serve the home page."""
    return render_template("index.html")


# Data browser routes
@data_bp.route("/data")
def list_data():
    """List available years in data directory."""
    data_path = Path(__file__).parent.parent / "data"
    years = []

    if data_path.exists():
        years = [d.name for d in data_path.iterdir() if d.is_dir() and d.name.isdigit()]
        years.sort(reverse=True)

    return render_template("data_years.html", years=years)


@data_bp.route("/data/<year>")
def list_year_data(year):
    """List available IDs for a specific year."""
    data_path = Path(__file__).parent.parent / "data" / year
    ids = []

    if data_path.exists():
        ids = [d.name for d in data_path.iterdir() if d.is_dir() and (d / "index.html").exists()]
        ids.sort()

    if not ids:
        abort(404)

    return render_template("data_ids.html", year=year, ids=ids)


@data_bp.route("/data/<year>/<id>")
def serve_data(year, id):
    """Serve index.html from data/year/id/ directory."""
    data_path = Path(__file__).parent.parent / "data" / year / id
    index_file = data_path / "index.html"

    if index_file.exists():
        return send_from_directory(data_path, "index.html")
    else:
        abort(404)


@data_bp.route("/data/<year>/<id>/<path:filename>")
def serve_data_files(year, id, filename):
    """Serve static files from data directories."""
    data_path = Path(__file__).parent.parent / "data" / year / id
    file_path = data_path / filename

    if file_path.exists() and file_path.is_file():
        return send_from_directory(data_path, filename)
    else:
        abort(404)


# Documentation route
@data_bp.route("/docs")
def docs():
    """Documentation page."""
    return render_template("docs.html")
