import appdirs
from pathlib import Path
from userContext import UserContext

from recodex_cli_lib.client import Client
import typer

config_dir = Path(appdirs.user_config_dir("recodex"))
data_dir = Path(appdirs.user_data_dir("recodex"))
context_path = data_dir / "context.yaml"

def getClient() -> Client:
    # show log in prompt if there is no session
    if not context_path.exists():
        user_context = login()
    # load session data
    else:
        user_context = UserContext.load(context_path)
        if user_context.is_token_expired:
            typer.echo("Token is expired, please log in to continue.")
            # use the old API url
            user_context = prompt_user_context(user_context.api_url)

    client = Client(user_context.api_token, user_context.api_url)

    # refresh token if necessary
    if user_context.is_token_almost_expired():
        user_context = user_context.replace_token(client.get_refresh_token())
        user_context.store(context_path)
        # recreate client
        client = Client(user_context.api_token, user_context.api_url)
    return client

def prompt_user_context(api_url) -> UserContext:
    username = typer.prompt("Username")
    password = typer.prompt("Password", hide_input=True)
    client = Client("", api_url)
    typer.echo("Connecting...")
    token = client.get_login_token(username, password)
    user_context = UserContext(api_url, token)
    user_context.store(context_path)
    typer.echo(f"Login token stored at: {context_path}")
    return user_context

def login() -> UserContext:
    api_url = typer.prompt("API URL")
    return prompt_user_context(api_url)
