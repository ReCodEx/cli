import clientFactory
import typer
import json

def call(endpoint: str, path: str, query: str, body: str):
    client = clientFactory.getClient()
    if endpoint.count(".") != 1:
        raise Exception("The endpoint needs to be in <presenter.handler> format.")
    
    try:
        path_parsed = json.loads(path)
        query_parsed = json.loads(query)
        body_parsed = json.loads(body)
    except:
        raise Exception("The JSON string is corrupted.")

    presenter, handler = endpoint.split(".")
    response = client.send_request(presenter, handler, body_parsed, path_parsed, query_parsed)
    print(response.data)
