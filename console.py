import typer
from typing_extensions import Annotated
import json

import clientFactory

app = typer.Typer()

@app.command()
def login():
    clientFactory.login()

@app.command()
def swagger():
    client = clientFactory.getClient()
    print(client.endpoint_resolver.get_swagger())

@app.command()
def call(
    endpoint: Annotated[
        str, typer.Argument(help="Endpoint identifier in <presenter.handler> format")
    ],
    path: Annotated[
        str, typer.Option(help="Path Parameters", rich_help_panel="Request Parameters")
    ] = "{}",
    query: Annotated[
        str, typer.Option(help="Query Parameters", rich_help_panel="Request Parameters")
    ] = "{}",
    body: Annotated[
        str, typer.Option(help="JSON Body", rich_help_panel="Request Parameters")
    ] = "{}",
):
    """Calls a ReCodEx endpoint with the provided parameters.
        Requires an endpoint identifier in <presenter.handler> format.
        Use --path, --query, and --body options to pass a json string representing the parameters.

    Raises:
        typer.Exit: Thrown when the argument or options are invalid.
    """
    client = clientFactory.getClient()
    if endpoint.count(".") != 1:
        typer.echo("The endpoint needs to be in <presenter.handler> format.")
        raise typer.Exit(1)
    
    try:
        path_parsed = json.loads(path)
        query_parsed = json.loads(query)
        body_parsed = json.loads(body)
    except:
        typer.echo("The JSON string is corrupted.")
        raise typer.Exit(1)

    presenter, handler = endpoint.split(".")
    response = client.send_request(presenter, handler, body_parsed, path_parsed, query_parsed)
    print(response.data)
    
if __name__ == "__main__":
    app()
    ###TODO: handle files
