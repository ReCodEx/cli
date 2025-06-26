import typer
from typing_extensions import Annotated
import typing
from collections.abc import Callable
from recodex_cli_lib.client import Client
import recodex_cli_lib.file_upload_helper as file_upload_helper

from ..utils import client_factory
from ..utils import cmd_utils as cmd_utils

app = typer.Typer()

@app.command()
def swagger(
    verbose: Annotated[
        bool, typer.Option(help="Execution Verbosity")
    ] = False,
):
    """Prints the swagger document currently used by the application.
    """
    client = client_factory.get_client_with_verbosity(verbose)
    print(client.endpoint_resolver.get_swagger())
