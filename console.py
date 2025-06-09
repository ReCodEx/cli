import typer
from typer_shell import make_typer_shell
from typing_extensions import Annotated
import typing
from collections.abc import Callable

from utils import client_factory
from recodex_cli_lib.client import Client
import call_command.command as cmd
import call_command.cmd_utils as cmd_utils
from call_command.command_state import CommandState

app = make_typer_shell(prompt="ReCodEx CLI: ", intro="Welcome to the ReCodEx Client Shell")
state = CommandState()

@app.command()
def swagger(
    verbose: Annotated[
        bool, typer.Option(help="Execution Verbosity", is_eager=True)
    ] = False,
):
    state.verbose = verbose
    client = get_client_with_verbosity()
    print(client.endpoint_resolver.get_swagger())

@app.command()
def call(
    endpoint: Annotated[
        str, typer.Argument(help="Endpoint identifier in <presenter.handler> format", is_eager=True)
    ] = "",
    path: Annotated[
        list[str], typer.Option(help="Pass a single PATH parameter", rich_help_panel="Request Parameters")
    ] = [],
    query: Annotated[
        list[str], typer.Option(help="Pass a single QUERY parameters in <key=value> format", rich_help_panel="Request Parameters")
    ] = [],
    body: Annotated[
        str, typer.Option(help="JSON or YAML request body (format detected automatically)", rich_help_panel="Request Parameters")
    ] = "{}",
    body_path: Annotated[
        str|None, typer.Option(help="If set, the request body will be read from the specified file (JSON or YAML)", allow_dash=True)
    ] = None,
    file: Annotated[
        str|None, typer.Option(help="Filepath to file to be uploaded", rich_help_panel="Request Parameters")
    ] = None,
    return_yaml: Annotated[
        bool, typer.Option(help="Whether to print the output in YAML format instead of JSON", allow_dash=True)
    ] = False,
    minimized: Annotated[
        bool, typer.Option(help="Whether the output should be minimized")
    ] = False,
    out_path: Annotated[
        str|None, typer.Option(help="If set, the output will be saved to this path", allow_dash=True)
    ] = None,
    verbose: Annotated[
        bool, typer.Option(help="Execution Verbosity", is_eager=True)
    ] = False,
    help: Annotated[
        bool, typer.Option(help="Display Help", callback=cmd.help_callback)
    ] = False,
):
    """Calls a ReCodEx endpoint with the provided parameters.

    Requires an endpoint identifier in <presenter.handler> format.

    Use --path options to pass PATH parameter values in order of definition,
    use --query options in <key=value> format to pass QUERY parameters,
    use --body to pass a JSON body.
    """
    
    # help is handled in call_command.help_callback
    if help:
        return
    
    state.verbose = verbose
    state.output_minimized = minimized
    state.output_path = out_path
    if return_yaml:
        state.output_format = "yaml"

    if file == None:
        file_obj = {}
    else:
        file_obj = {"file": file}

    client = get_client_with_verbosity()

    if endpoint == "":
        command = lambda: cmd.call_interactive(client, state)
    else:
        def command():
            if body_path == None:
                parsed_body = cmd_utils.parse_input_body(body)
            else:
                parsed_body = cmd_utils.parse_input_body_file(body_path)
            cmd.call(client, endpoint, path, query, parsed_body, state, files=file_obj)

    execute_with_verbosity(command)


def get_client_with_verbosity() -> Client:
    return execute_with_verbosity(client_factory.get_client)

def execute_with_verbosity(command: Callable[[], typing.Any]):
    return cmd_utils.execute_with_verbosity(command, state.verbose)

if __name__ == "__main__":
    app()
