import typer
import click
from typing_extensions import Annotated
import json
import sys
from collections.abc import Callable

import clientFactory
import commands

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
    query_json: Annotated[
        str, typer.Option(help="Query Parameters", rich_help_panel="Request Parameters")
    ] = "{}",
    query: Annotated[
        list[str], typer.Option(help="Query Parameters", rich_help_panel="Request Parameters", allow_dash=True)
    ] = [],
    body: Annotated[
        str, typer.Option(help="JSON Body", rich_help_panel="Request Parameters")
    ] = "{}",
    verbose: Annotated[
        bool, typer.Option(help="Execution Verbosity")
    ] = False,
):
    """Calls a ReCodEx endpoint with the provided parameters.
    Requires an endpoint identifier in <presenter.handler> format.
    Use --path, --query, and --body options to pass a json string representing the parameters.
    """

    print(query)

    command = lambda: commands.call(endpoint, path, query_json, body)
    execute_with_verbosity(command, verbose)
    
def execute_with_verbosity(command: Callable[[], None], verbose: bool):
    if verbose:
        command()
    else:
        try:
            command()
        except Exception as e:
            raise click.ClickException(str(e))

if __name__ == "__main__":
    app()
    ###TODO: handle files
