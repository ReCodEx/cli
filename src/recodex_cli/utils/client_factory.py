import typer
from recodex_cli_lib import client_factory
from recodex_cli_lib.client import Client

from .cmd_utils import execute_with_verbosity


def logout(verbose=False):
    client_factory.remove_session()


def login_with_prompt(verbose=False):
    user_context = client_factory.load_user_context()

    if user_context is None or user_context.api_url is None:
        api_url = typer.prompt("API URL")
        username = typer.prompt("Username")
        password = typer.prompt("Password", hide_input=True)
        client_factory.create_session_from_credentials(api_url, username, password, verbose)
    elif user_context.is_token_expired:
        username = typer.prompt("Username")
        password = typer.prompt("Password", hide_input=True)
        client_factory.create_session_from_credentials(user_context.api_url, username, password, verbose)
    else:
        print("Already logged in")


def login_with_token(api_token: str, api_url: str | None = None, verbose=False):
    api_url = __get_primary_api_url(api_url)
    client_factory.create_session_from_token(api_url, api_token, verbose)  # type: ignore


def login_with_credentials(username: str, password: str, api_url: str | None = None, verbose=False):
    api_url = __get_primary_api_url(api_url)
    client_factory.create_session_from_credentials(api_url, username, password)


def get_client_with_verbosity(verbose: bool) -> Client:
    """Creates a client object. If the user context file is missing or expired,
    prompts the user via CLI for login credentials.

    Args:
        verbose (bool): Whether to truncate error messages.

    Returns:
        Client: Returns a client object.
    """

    return execute_with_verbosity(client_factory.get_client_from_session, verbose)


def __get_primary_api_url(api_url: str | None) -> str:
    user_context = client_factory.load_user_context()

    if user_context is None and api_url is None:
        raise Exception("Please provide the URL of the host.")
    elif user_context is not None and api_url is None:
        if user_context.api_url is None:
            raise Exception("Please provide the URL of the host.")
        api_url = user_context.api_url

    return api_url  # type: ignore
