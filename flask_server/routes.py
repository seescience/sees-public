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

from flask import Blueprint, request, abort, render_template, render_template_string, send_from_directory, g, url_for, current_app

from .search import reset_index, index_all_data, query_index
from .forms import SearchForm

# Create blueprint for data routes
data_bp = Blueprint("data", __name__)

# Base directory (Archives)
base_dir = Path("/Volumes/public")

@data_bp.before_app_request
def before_request():
    g.search_form = SearchForm()


# Home route
@data_bp.route("/")
def home():
    """Serve the home page."""
    return render_template("index.html")


# Data browser routes
@data_bp.route("/data/old")
def list_data():
    """List available years in data directory."""
    data_path = base_dir / "data"
    years = []

    if data_path.exists():
        years = [d.name for d in data_path.iterdir() if d.is_dir() and d.name.isdigit()]
        years.sort(reverse=True)

    return render_template("data_years.html", years=years)

# List all data and add it to an elasticsearch index
@data_bp.route("/data")
def list_data_indexed():
    index_name = current_app.config["INDEX_NAME"]
    posts_per_page = int(current_app.config["POSTS_PER_PAGE"])
    # Filter params
    # sort_col = request.args.get("sort", "id")
    # sort_order = request.args.get("order", "desc")
    # selected_year = request.args.get("year", "2026")
    # Validation
    # if sort_col not in ["id", "title", "author", "year"]:
        # sort_col = "year"
    # If the index doesn't already exist, create it
    page = request.args.get('page', 1, type=int)
    query = request.args.get('q', None, type=str)
    if not current_app.elasticsearch.indices.exists(index=index_name):
        reset_index(index_name)
    q = g.search_form.q.data if query else None
    data, total = query_index(index_name, q, page, posts_per_page)
    # Search the folder and update the index to include all data
    index_all_data(base_dir / "data", index_name, [d['_id'] for d in data])
    next_url = url_for('data.list_data_indexed', q=q, page=page + 1) if total > page * posts_per_page else None
    prev_url = url_for('data.list_data_indexed', q=q, page=page - 1) if page > 1 else None
    # Filter by selected year
    all_years = sorted({row["_source"]["year"] for row in data}, reverse=True)
    # if selected_year:
        # data = [row for row in data if str(row["year"]) == selected_year]
    # Sort data
    if q:
        data = sorted(data, key=lambda x: int(x["_score"]), reverse=True)
    else:
        data = sorted(data, key=lambda x: int(x["_id"]), reverse=True)
    # reverse = sort_order == "desc"
    # data = sorted(data, key=lambda x: x[sort_col], reverse=reverse)
    # Call render_template and pass the list of all documents
    return render_template("data.html", data=[row["_source"] for row in data], years=all_years, next_url=next_url, prev_url=prev_url)
    # return render_template("data.html", data=data, years=all_years, sort_col=sort_col, sort_order=sort_order, selected_year=selected_year)
    # return render_template("data_ids.html", year=1970, data=[x["id"] for x in data])

# TODO: Create endpoint for getting search results from query
# For being called from JS
# Read chapters on pagination and AJAX


# List data filtered by a search
# replaced this code with a request arg in the /data route
"""
@data_bp.route("/data/search")
def search():
    if not g.search_form.validate():
        return redirect(url_for("data.list_data_indexed"))
    if not g.search_form.q.data:
        return redirect(url_for("data.list_data_indexed"))
    page = request.args.get('page', 1, type=int)
    data, total = query_index(index_name, g.search_form.q.data, page, current_app.config['POSTS_PER_PAGE'])
    data = sorted(data, key=lambda x: int(x["_score"]), reverse=True)
    documents = [hit["_source"] for hit in data]
    all_years = sorted({row["year"] for row in documents}, reverse=True)
    return render_template("data.html", data=documents, years=all_years)
"""

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
