import typer
from recodex_cli_lib import client_factory
from recodex_cli_lib.client import Client

from .cmd_utils import execute_with_verbosity

def get_client() -> Client:
    """Creates a client object. If the user context file is missing or expired,
    prompts the user via CLI for login credentials.

    Returns:
        Client: Returns a client object.
    """

    user_context = client_factory.load_user_context()
    
    # show log in prompt if there is no session
    if user_context == None:
        api_url = typer.prompt("API URL")
        username = typer.prompt("Username")
        password = typer.prompt("Password", hide_input=True)
        return client_factory.get_client(api_url, username, password, verbose=True)
    
    if user_context.is_token_expired:
        username = typer.prompt("Username")
        password = typer.prompt("Password", hide_input=True)
        return client_factory.get_client(user_context.api_url, username, password, verbose=True)
    
    return client_factory.get_client_from_user_context(user_context)

def get_client_with_verbosity(verbose: bool) -> Client:
    return execute_with_verbosity(get_client, verbose)
