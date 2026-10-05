#!/usr/bin/env python3
# ----------------------------------------------------------------------------------
# Project: SEES Public
# File: flask_server/search.py
# ----------------------------------------------------------------------------------
# Purpose:
# This file contains utility functions related to ElasticSearch.
# ----------------------------------------------------------------------------------
# Author: Alexander Nicolellis
#
# Copyright (C) 2026 GSECARS, The University of Chicago, USA
# Copyright (C) 2026 NSF SEES, USA
# ----------------------------------------------------------------------------------

from flask import current_app
from bs4 import BeautifulSoup
from elasticsearch import helpers

# Constructs a document containing the data of the ESAF found at the specified file path
# Indexes the ESAF in ElasticSearch
# Indexed fields: title, author, id, year
# Returns the payload
def add_to_index(index_name, id, year, file_path):
    # Parse index.html file into payload
    payload = parse_data_from_html(file_path)
    payload["id"] = id
    payload["year"] = year
    current_app.elasticsearch.index(index=index_name, id=id, document=payload)
    return payload

# Returns all data that result from the given query
# If no query is given, returns all data from ElasticSearch
# Also returns the number of hits
def query_index(index, query):
    if not query:
        search = current_app.elasticsearch.search(index=index, query={"match_all": {}}, size=2000)
    else:
        search = current_app.elasticsearch.search(index=index, query={"multi_match": {"query": query, "fields": ["*"]}}, size=2000)
    hits = search['hits']['hits']
    return hits, search['hits']['total']['value']

# Return all data ids that result from the given query
# Returns all ids if no query is given
def query_index_paginated(index, query, page, per_page):
    if not query:
        search = current_app.elasticsearch.search(index=index, query={"match_all": {}}, from_=(page-1)*per_page, size=per_page)
    else:
        search = current_app.elasticsearch.search(index=index, query={"multi_match": {"query": query, "fields": ["*"]}}, from_=(page-1)*per_page, size=per_page)
    hits = search['hits']['hits']
    return hits, search['hits']['total']['value']

# For the index.html file located at the specified path, retrieve the data for the search index
# Current fields being parsed: title, author
def parse_data_from_html(file_path):
    f = open(file_path)
    doc = BeautifulSoup(f, "html.parser")
    title = doc.find("h2", class_="dataset-title").get_text()
    author = doc.find("table", class_="dataset-table").find_all("tr")[3].find_all("td")[1].get_text()

    return {"title": title, "author":author}

# Returns a list of ID numbers for all data in the index
def get_all_indexed_ids(index_name):
    hits = helpers.scan(current_app.elasticsearch, query={"query":{"match_all": {}}}, index=index_name)
    return [hit['_id'] for hit in hits]

# Retrieve all indexed documents
def get_all_docs(index_name):
    hits = helpers.scan(current_app.elasticsearch, query={"query":{"match_all": {}}}, index=index_name)
    return [hit["_source"] for hit in hits]

# Reinstantiate the elasticsearch index with the given name
def reset_index(index_name):
    # Delete without giving an error if the index doesn't exist
    current_app.elasticsearch.indices.delete(index=index_name, ignore_unavailable=True)
    current_app.elasticsearch.indices.create(index=index_name)

# Traverse the data_path folder. Check if any folders are not already in the index.
# Updates the elasticsearch index with any new data.
def index_all_data(data_path, index_name, ids=None):
    years = []

    if not data_path.exists():
        print("Error: data path not found")

    years = [d.name for d in data_path.iterdir() if d.is_dir() and d.name.isdigit()]

    prev_ids = get_all_indexed_ids(index_name)

    for year in years:
        path = data_path / year

        for d in path.iterdir():
            if d.is_dir() and (d / "index.html").exists() and d.name not in prev_ids and (d.name in ids or not ids):
                add_to_index(index_name, d.name, year, d / "index.html")
