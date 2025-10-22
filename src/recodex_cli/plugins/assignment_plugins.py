import typer
from typing_extensions import Annotated
from recodex.generated.swagger_client.api.default_api import DefaultApi

from ..utils import client_factory
from ..utils import cmd_utils as cmd_utils

app = typer.Typer()

@app.command()
def update(
    assignment_id: Annotated[
        str, typer.Argument(help="Assignment ID")
    ],
    body_path: Annotated[
        str | None, typer.Option(
            help="Path to JSON body with settings to be changed",
            allow_dash=False
        )
    ],
    verbose: Annotated[
        bool, typer.Option(help="Execution Verbosity")
    ] = False,
):
    """Updates given assignment settings without the need to specify all required parameters.
    Required parameters that are not specified remain unchanged
    """
    client = client_factory.get_client_with_verbosity(verbose)

    def get_assignment_details(aid):
        command = lambda: client.send_request_by_callback(DefaultApi.assignments_presenter_action_detail, path_params={ "id": aid })
        response = cmd_utils.execute_with_verbosity(command, verbose)
        return response.get_payload()

    endpoint_definition = client.endpoint_resolver.get_endpoint_definition('assignments', 'update_detail')
    required_params = { i: None for i in endpoint_definition['requestBody']['content']['application/json']['schema']['required'] }
    requested_updates = cmd_utils.parse_input_body_file(body_path)

    new_data = required_params | requested_updates

    assignment_data = get_assignment_details(assignment_id)

    for key in new_data.keys():
        if new_data[key] is None:
            new_data[key] = assignment_data[key]

    # ToDo: API doesn't seem care if there are extra/non-defined/non-documented/mistyped json arguments.
    #       Maybe validate new_data on endpoint_definition scheme and throw error like 'unknown parameter: %s'

    command = lambda: client.send_request_by_callback(DefaultApi.assignments_presenter_action_update_detail, path_params={ "id": assignment_id }, body=new_data)
    cmd_utils.execute_with_verbosity(command, verbose)
