import typer
from typing_extensions import Annotated
import click

from .utils import client_factory
from .utils import cmd_utils as cmd_utils
from .call_command import command as cmd
from .call_command.command_state import CommandState
from .plugins import file_plugins, info_plugins

app = typer.Typer()
state = CommandState()

# register plugins
app.add_typer(file_plugins.app, name="file")
app.add_typer(info_plugins.app, name="info")


@app.command()
def call(
    endpoint: Annotated[
        str, typer.Argument(help="Endpoint identifier in <presenter.action> format", is_eager=True)
    ] = "",
    path: Annotated[
        list[str], typer.Option(help="Pass a single PATH parameter", rich_help_panel="Request Parameters")
    ] = [],
    query: Annotated[
        list[str], typer.Option(
            help="Pass a single QUERY parameters in <name=value> format",
            rich_help_panel="Request Parameters"
        )
    ] = [],
    body: Annotated[
        str, typer.Option(
            help="JSON or YAML request body (format detected automatically)",
            rich_help_panel="Request Parameters"
        )
    ] = "{}",
    body_path: Annotated[
        str | None, typer.Option(
            help="If set, the request body will be read from the specified file (JSON or YAML)",
            allow_dash=True
        )
    ] = None,
    file: Annotated[
        str | None, typer.Option(help="Filepath to file to be uploaded", rich_help_panel="Request Parameters")
    ] = None,
    return_yaml: Annotated[
        bool, typer.Option(help="Whether to print the output in YAML format instead of JSON", allow_dash=True)
    ] = False,
    return_raw: Annotated[
        bool, typer.Option(help="Whether to print the raw, unparsed output", allow_dash=True)
    ] = False,
    minimized: Annotated[
        bool, typer.Option(help="Whether the output should be minimized")
    ] = False,
    out_path: Annotated[
        str | None, typer.Option(help="If set, the output will be saved to this path", allow_dash=True)
    ] = None,
    verbose: Annotated[
        bool, typer.Option(help="Execution Verbosity", is_eager=True)
    ] = False,
    help: Annotated[
        bool, typer.Option(help="Display Help", callback=cmd.help_callback)
    ] = False,
):
    """Calls a ReCodEx endpoint with the provided parameters.

    Requires an endpoint identifier in <presenter.action> format.

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

    if return_yaml and return_raw:
        click.ClickException("--return-yaml and --return-raw cannot be used both at the same time")
    if return_yaml:
        state.output_format = "yaml"
    elif return_raw:
        state.output_format = "raw"

    if file is None:
        file_obj = {}
    else:
        file_obj = {"file": file}

    client = client_factory.get_client_with_verbosity(state.verbose)

    if endpoint == "":
        def command():
            lambda: cmd.call_interactive(client, state)
    else:
        def command():
            if body_path is None:
                parsed_body = cmd_utils.parse_input_body(body)
            else:
                parsed_body = cmd_utils.parse_input_body_file(body_path)
            cmd.call(client, endpoint, path, query, parsed_body, state, files=file_obj)

    cmd.cmd_utils.execute_with_verbosity(command, state.verbose)


if __name__ == "__main__":
    app()
