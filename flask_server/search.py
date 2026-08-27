from flask import current_app
from bs4 import BeautifulSoup

# Add all specified fields to the search index of the file located at the path
def add_to_index(index_name, id, file_path):
    # Parse index.html file into payload
    payload = parse_data_from_html(file_path)
    payload["id"] = id
    current_app.elasticsearch.index(index=index_name, id=id, document=payload)
    return payload

# Return all data ids that result from the given query
def query_index(index, query):
    search = current_app.elasticsearch.search(index=index, query={"multi_match": {"query": query, "fields": ["*"]}})
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids, search['hits']['total']['value']

# For the index.html file located at the specified path, retrieve the data for the search index
# Current fields: title, author
def parse_data_from_html(file_path):
    f = open(file_path)
    doc = BeautifulSoup(f, "html.parser")
    title = doc.find("h2", class_="dataset-title").get_text()
    author = doc.find("table", class_="dataset-table").find_all("tr")[3].find_all("td")[1].get_text()

    return {"title": title, "author":author}

def reset_index(index_name):
    current_app.elasticsearch.indices.delete(index=index_name, ignore_unavailable=True)
    current_app.elasticsearch.indices.create(index=index_name)

def index_all_data(data_path, index_name):
    years = []

    if not data_path.exists():
        print("Error: data path not found")

    years = [d.name for d in data_path.iterdir() if d.is_dir() and d.name.isdigit()]

    data = []

    for year in years:
        path = data_path / year

        for d in path.iterdir():
            if d.is_dir() and (d / "index.html").exists():
                html_path = path / d / "index.html"
                obj = add_to_index(index_name, d.name, html_path)
                data.append(obj)

    return data
