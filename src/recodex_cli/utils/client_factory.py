import typer
from recodex_cli_lib import client_factory
from recodex_cli_lib.client import Client

from .cmd_utils import execute_with_verbosity


def logout(verbose=False):
    """Removes the local user context file, effectively logging the user out.

    Args:
        verbose (bool, optional): Execution verbosity. Defaults to False.
    """

    client_factory.remove_session()


def login_with_prompt(verbose=False):
    """Displays a prompt that will query the credentials of the user. In case the user is already logged in,
        the prompt will not be displayed.

    Args:
        verbose (bool, optional): Execution verbosity. Defaults to False.
    """

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
    """Creates a user context file from an API token.

    Args:
        api_token (str): The API token.
        api_url (str | None, optional): The API URL of the server. If not provided, the URL from
            the old context file will be retrieved, if it exists. Defaults to None.
        verbose (bool, optional): Execution verbosity. Defaults to False.
    """

    api_url = __get_primary_api_url(api_url)
    client_factory.create_session_from_token(api_url, api_token, verbose)  # type: ignore


def login_with_credentials(username: str, password: str, api_url: str | None = None, verbose=False):
    """Creates a user context file from credentials.

    Args:
        username (str): The username of the user.
        password (str): The password of the user.
        api_url (str | None, optional): The API URL of the server. If not provided, the URL from
            the old context file will be retrieved, if it exists. Defaults to None.
        verbose (bool, optional): Execution verbosity. Defaults to False.
    """

    api_url = __get_primary_api_url(api_url)
    client_factory.create_session_from_credentials(api_url, username, password, verbose)


def get_client_with_verbosity(verbose: bool) -> Client:
    """Creates a client object from the local user context file.

    Args:
        verbose (bool): Whether to truncate error messages.

    Returns:
        Client: Returns a client object.
    """

    return execute_with_verbosity(client_factory.get_client_from_session, verbose)


def __get_primary_api_url(api_url: str | None) -> str:
    """Returns a not None API URL, primarily the function parameter, secondarily the URL from the user context file.
    Args:
        api_url (str | None): The API URL retrieved from the CLI.

    Raises:
        Exception: Thrown when both sources are None.

    Returns:
        str: Returns the API URL to the ReCodEx server.
    """

    user_context = client_factory.load_user_context()

    if user_context is None and api_url is None:
        raise Exception("Please provide the URL of the host.")
    elif user_context is not None and api_url is None:
        if user_context.api_url is None:
            raise Exception("Please provide the URL of the host.")
        api_url = user_context.api_url

    return api_url  # type: ignore
