import typer
import click
from typing_extensions import Annotated
import json
import sys
from collections.abc import Callable

from recodex_cli_lib import client_factory
from recodex_cli_lib.endpoint_resolver import EndpointResolver
import call_command

app = typer.Typer()
state = { "verbose" : False }

@app.command()
def swagger():
    client = client_factory.get_client_interactive()
    print(client.endpoint_resolver.get_swagger())

@app.command()
def call(
    endpoint: Annotated[
        str, typer.Argument(help="Endpoint identifier in <presenter.handler> format")
    ] = "",
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
    state["verbose"] = verbose
    client = client_factory.get_client_interactive()

    if endpoint == "":
        command = lambda: call_command.call_interactive(client)
    else:
        #TODO: handle other params
        parsed_body = call_command.parse_json(body)
        command = lambda: call_command.call(client, endpoint, {}, {}, parsed_body)

    execute_with_verbosity(command)

def execute_with_verbosity(command: Callable[[], None]):
    try:
        command()
    except Exception as e:
        if state["verbose"]:
            raise e
        else:
            raise click.ClickException(str(e))

if __name__ == "__main__":
    app()
    ###TODO: handle files
