from flask import current_app
from bs4 import BeautifulSoup

# Add all specified fields to the search index of the file located at the path
def add_to_index(index, id, file_path):
    # Parse index.html file into payload
    payload = parse_data_from_html(file_path)
    payload["id"] = id
    current_app.elasticsearch.index(index=index, id=id, document=payload)

# Return all data ids that result from the given query
def query_index(index, query):
    search = current_app.elasticsearch.search(index=index, query={"multi_match": {"query": query, "fields": ["*"]}})
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids, search['hits']['total']['value']

# For the index.html file located at the specified path, retrieve the data for the search index
# Current fields: title, author
def parse_data_from_html(file_path):
    doc = BeautifulSoup(file_path, "html.parser")
    title = doc.find("dataset-title")
    author = doc.find("dataset-table").find_all("tr")[3].find_all("td")[1].get_text()

    return {"title": title, "author":author}