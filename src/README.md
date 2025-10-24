# Development documentation

## Code Structure

The main entry point is the `console.py` file located in `src/recodex_cli`.
It registers all plugin files and defines the `call`, `login`, and `logout` commands.

All plugins are stored in the `plugins` folder.

The `call_command` folder contains the implementation of the `call` command, notably input parsing, help message generation, and response formatting.

## Writing Plugins

New plugins can be added to the existing plugin files or new ones.
In case you create a new plugin file, do not forget to register it in `console.py`.

The following skeleton implementation can be used as the basis for new commands:

```python
import typer
# import the DefaultApi class that holds all request functions
from recodex.generated.swagger_client.api.default_api import DefaultApi

from ..utils import client_factory
from ..utils import cmd_utils as cmd_utils

# make a Typer object that will be registered in console.py
app = typer.Typer()


@app.command()
def new_command(
    # define positional arguments
    arg: Annotated[
        str, typer.Argument(help="Command argument")
    ],
    # add options
    verbose: Annotated[
        bool, typer.Option(help="Execution Verbosity")
    ] = False,
):
    # get the client object used to send requests
    client = client_factory.get_client_with_verbosity(verbose)

    # send requests (optionally wrap the requests in a lambda)
    command = lambda: client.send_request_by_callback(DefaultApi.login_presenter_action_default)

    # pass the lambda to this utility function to print shorter
    # error messages unless the verbose flag is set (optional)
    response = cmd_utils.execute_with_verbosity(command, verbose)
    
    print(response)
```
