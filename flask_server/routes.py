#!/usr/bin/env python3
# ----------------------------------------------------------------------------------
# Project: SEES Public
# File: flask_server/routes.py
# ----------------------------------------------------------------------------------
# Purpose:
# This file contains all the Flask routes for serving dynamic data content.
# ----------------------------------------------------------------------------------
# Author: Christofanis Skordas, Alexander Nicolellis
#
# Copyright (C) 2025 GSECARS, The University of Chicago, USA
# Copyright (C) 2025 NSF SEES, USA
# ----------------------------------------------------------------------------------

#!/usr/bin/env python3
from pathlib import Path
import json

from flask import Blueprint, request, abort, render_template, render_template_string, current_app

from .search import reset_index, index_all_data, query_index

# Create blueprint for data routes
data_bp = Blueprint("data", __name__)

# Base directory (Archives)
base_dir = Path("/Volumes/public")


# Home route
@data_bp.route("/")
def home():
    """Serve the home page."""
    return render_template("index.html")


# Route for the Data page
@data_bp.route("/data")
def list_data_indexed():
    index_name = current_app.config["INDEX_NAME"]
    # Get query from request params.
    # This is currently not directly used, but allows users to manually search from the URL.
    q = request.args.get("q", "", type=str)
    # If the index doesn't already exist, create it
    if not current_app.elasticsearch.indices.exists(index=index_name):
        reset_index(index_name)
    # Get data to render from ElasticSearch filtered by the query
    data, _ = query_index(index_name, q)
    ids = [d["_id"] for d in data]
    # Search the folder and update the index to include all data
    post = index_all_data(base_dir / "data", index_name, ids, q)
    if post:
        data = post
    # Get all years present in the data
    all_years = sorted({row["_source"]["year"] for row in data}, reverse=True)
    # Sort data by search score if a query is used. Otherwise, sort by ID number
    if q != "":
        data = sorted(data, key=lambda x: int(x["_score"]), reverse=True)
    else:
        data = sorted(data, key=lambda x: int(x["_id"]), reverse=True)
    # Call render_template and pass the list of all documents and year numbers
    return render_template("data.html", data=[row["_source"] for row in data], years=all_years)


# Endpoint for getting search results from query
# For being called from JS
@data_bp.route("/search", methods=["POST"])
def search():
    index_name = current_app.config["INDEX_NAME"]
    query = request.get_json()["text"]
    data, total = query_index(index_name, query)
    if query != "":
        data = sorted(data, key=lambda x: int(x["_score"]), reverse=True)
    else:
        data = sorted(data, key=lambda x: int(x["_id"]), reverse=True)
    return json.dumps([row["_source"] for row in data])


# Directly render a specific file
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


# Documentation route
@data_bp.route("/docs")
def docs():
    """Documentation page."""
    return render_template("docs.html")
