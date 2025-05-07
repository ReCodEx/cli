import typer
import click
from rich.console import Console
from rich.panel import Panel
import typer.cli
import typer.core
import typer.utils
from typing_extensions import Annotated
import json
import sys
import typing
from collections.abc import Callable

import inspect

from recodex_cli_lib import client_factory
from recodex_cli_lib.endpoint_resolver import EndpointResolver
from recodex_cli_lib.client import Client
import call_command

app = typer.Typer()
state = { "verbose" : False }

@app.command()
def swagger(
):
    client = client_factory.get_client_interactive()
    print(client.endpoint_resolver.get_swagger())

@app.command()
def call(
    endpoint: Annotated[
        str, typer.Argument(help="Endpoint identifier in <presenter.handler> format", is_eager=True)
    ] = "",
    path: Annotated[
        list[str], typer.Option(help="Path Parameters", rich_help_panel="Request Parameters")
    ] = [],
    query: Annotated[
        list[str], typer.Option(help="Query Parameters", rich_help_panel="Request Parameters")
    ] = [],
    body: Annotated[
        str, typer.Option(help="JSON Body", rich_help_panel="Request Parameters")
    ] = "{}",
    verbose: Annotated[
        bool, typer.Option(help="Execution Verbosity", is_eager=True)
    ] = False,
    help: Annotated[
        bool, typer.Option(help="Display Help", callback=call_command.help_callback)
    ] = False,
):
    """Calls a ReCodEx endpoint with the provided parameters.
    Requires an endpoint identifier in <presenter.handler> format.
    Use --path, --query, and --body options to pass a json string representing the parameters.
    """
    
    # help is handled in call_command.help_callback
    if help:
        return
    
    state["verbose"] = verbose
    client = get_client_with_verbosity()

    if endpoint == "":
        command = lambda: call_command.call_interactive(client, verbose)
    else:
        #TODO: handle other params
        parsed_body = call_command.parse_json(body)
        command = lambda: call_command.call(client, endpoint, path, {}, parsed_body, verbose)

    execute_with_verbosity(command)

def get_client_with_verbosity() -> Client:
    return execute_with_verbosity(client_factory.get_client_interactive)

def execute_with_verbosity(command: Callable[[], typing.Any]):
    return call_command.execute_with_verbosity(command, state["verbose"])

if __name__ == "__main__":
    app()
    ###TODO: handle files
