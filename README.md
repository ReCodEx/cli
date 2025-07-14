# ReCodEx Client

A command-line interface for the [ReCodEx](https://recodex.mff.cuni.cz/) system. This tool allows users to interact with ReCodEx from their terminal, streamlining workflows and enabling scripting possibilities.

## What is ReCodEx?

ReCodEx is a system for dynamic analysis and evaluation of programming exercises. It allows supervisors to assign programming problems to students, who can then submit their solutions through a web interface. ReCodEx automatically evaluates these solutions by compiling and executing them in a safe environment, providing quick feedback to students.

## Key Features

* **Authentication:** Securely log in to your ReCodEx account. The CLI will securely store your access token for future sessions.
* **Execute Requests:** Send requests and view responses from the command line.
* **Interactive Mode:** You can use the interactive mode to browse and use existing endpoints.
* **Plugins:** Use existing plugins or write your own to streamline your work.

## Installation

The recommended way to install the ReCodEx CLI is via `pip`. Python 3.11 is recommended, but other versions may also work:

```bash
PIP_EXTRA_INDEX_URL="https://test.pypi.org/simple/" pip install recodex_cli_eceltov
```

### Installation from Source

For developers or those who prefer to install directly from the source code, follow these steps:

```bash
# make sure to run these commands from the root of the repository
./commands/initRepo.sh
source venv/bin/activate
```

## Getting Started

- **Login:** You can login with your credentials or an API token. When no command options are specified, an interactive prompt will be shown that will query your credentials.

    ```bash
    # login with credentials
    python3 -m recodex_cli login --username test --password test --api-url http://localhost:4000 --verbose

    # login with API token
    python3 -m recodex_cli login --api-url http://localhost:4000 --token eyJ... --verbose

    # login with credentials via prompts
    python3 -m recodex_cli login

    # logout
    python3 -m recodex_cli logout
    ```

- **Explore Commands:** You can view the full list of available commands and options by running:

    ```bash
    python3 -m recodex_cli --help
    ```

## Usage

### Call Command

The client defines the `call` command, which can be used to call any endpoint.

- **Interactive Mode:** By calling the command without any arguments, an interactive query will start that will prompt you for what endpoint you want to call and its parameters.


    ```bash
    python3 -m recodex_cli call
    ```

- **Calling an Endpoint:** To call an endpoint, add an argument in the `presenter.action` format, followed by any request parameters.

    ```bash
    # use QUERY parameters in <name=value> format
    python3 -m recodex_cli call groups.default --query search=Demo

    # you can pass a JSON or YAML file as a request body
    python3 -m recodex_cli call registration.create_invitation --body-path invite.yaml

    # PATH parameters are used in order of declaration (the first one is usually the ID)
    python3 -m recodex_cli call groups.set_organizational --path 10000000-2000-4000-8000-160000000000 --body '{"value":true}'
    ```

- **Help:** To print a detailed description on how to use the command, use:

    ```bash
    python3 -m recodex_cli call --help
    ```

    You can also view all parameters of a specific command.

    ```bash
    python3 -m recodex_cli call groups.default --help
    ```

### Plugins

The client can also be extended with plugins that can streamline common request patterns.

- **File Upload:**  Files can be uploaded simply by providing a path. Larger files will automatically be fragmented into chunks.

    ```bash
    python3 -m recodex_cli file upload test.csv 
    > File sent successfully
    > File ID: 73aac159-b2e2-402b-9e19-096f3ec0ae7c
    ```

- **File Download:** 
    ```bash
    python3 -m recodex_cli file download 73aac159-b2e2-402b-9e19-096f3ec0ae7c --out-path test.csv
    ```

- **Get Swagger:** This command returns the Swagger document (OpenAPI Specification) currently used by the client.

    ```bash
    python3 -m recodex_cli info swagger
    ```

## Development

### Code Structure

The main entry point is the `console.py` file located in `src/recodex_cli`.
It registers all plugin files and defines the `call`, `login`, and `logout` commands.

All plugins are stored in the `plugins` folder.

The `call_command` folder contains the implementation of the `call` command, notably input parsing, help message generation, and response formatting.

### Writing Plugins

New plugins can be added to the existing plugin files or new ones.
In case you create a new plugin file, do not forget to register it in `console.py`.

The following skeleton implementation can be used as the basis for new commands:

```python
import typer
# import the DefaultApi class that holds all request functions
from recodex_cli_lib.generated.swagger_client.api.default_api import DefaultApi

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

### Publishing

Use the `commands/uploadPackage.sh` script to upload a new version of the client.
Note that this will require a PyPI account and upload privileges.