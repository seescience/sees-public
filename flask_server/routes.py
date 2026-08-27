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

from flask import Blueprint, abort, render_template, render_template_string, send_from_directory

from .search import reset_index, index_all_data

# Create blueprint for data routes
data_bp = Blueprint("data", __name__)

# Base directory
base_dir = Path("/Volumes/public")


# Home route
@data_bp.route("/")
def home():
    """Serve the home page."""
    return render_template("index.html")


# Data browser routes
@data_bp.route("/data")
def list_data():
    """List available years in data directory."""
    data_path = base_dir / "data"
    years = []

    if data_path.exists():
        years = [d.name for d in data_path.iterdir() if d.is_dir() and d.name.isdigit()]
        years.sort(reverse=True)

    return render_template("data_years.html", years=years)

# List all data and add it to an elasticsearch index
@data_bp.route("/data/test")
def list_data_indexed():
    # Traverse base_dir/data and for each index.html file, add it to the index
    reset_index("test")
    data = index_all_data(base_dir / "data", "test")

    # Call render_template and pass the list of all documents
    #return render_template("data.html", data)
    return render_template("data_ids.html", year=1970, ids=[x["id"] for x in data])


@data_bp.route("/data/<year>")
def list_year_data(year):
    """List available IDs for a specific year."""
    data_path = base_dir / "data" / year
    ids = []

    if data_path.exists():
        ids = [d.name for d in data_path.iterdir() if d.is_dir() and (d / "index.html").exists()]
        ids.sort()

    if not ids:
        abort(404)

    return render_template("data_ids.html", year=year, ids=ids)


@data_bp.route("/data/<year>/<id>")
@data_bp.route("/data/<year>/<id>/")
def serve_data(year, id):
    """Render index.html from data/year/id/ directory as a template."""
    data_path = base_dir / "data" / year / id
    index_file = data_path / "index.html"

    if index_file.exists():
        # Read the HTML file content
        with open(index_file, "r", encoding="utf-8") as f:
            template_content = f.read()

        # Render it as a Jinja2 template
        return render_template_string(template_content)
    else:
        abort(404)


@data_bp.route("/data/<year>/<id>/<path:filename>")
def serve_data_files(year, id, filename):
    """Serve static files from data directories."""
    data_path = base_dir / "data" / year / id
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
