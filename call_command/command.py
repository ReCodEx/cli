from recodex_cli_lib.client import Client
from recodex_cli_lib.endpoint_resolver import EndpointResolver
import typer
import inquirer
import click

from call_command.response_printer import print_response
import call_command.cmd_utils as cmd_utils
from call_command.help_printer import HelpPrinter
from call_command.command_state import CommandState

def call_interactive(client: Client, state: CommandState):
    # start an interactive prompt if there is no endpoint
    endpoint_resolver = EndpointResolver()
    presenter, handler = prompt_endpoint(endpoint_resolver)
    endpoint = f"{presenter}.{handler}"
    path_param_values, query_param_values, body_string = prompt_request_data(endpoint_resolver, presenter, handler)
    body = cmd_utils.parse_json(body_string)
    
    call(client, endpoint, path_param_values, query_param_values, body, state)

def call(client: Client, endpoint: str, path_values: list[str], query_values: list[str], body: dict, state: CommandState):
    presenter, handler = cmd_utils.parse_endpoint_or_throw(endpoint)

    # parse params
    path_dict = path_list_to_dict(client.endpoint_resolver, presenter, handler, path_values)
    query_dict = query_list_to_dict(client.endpoint_resolver, presenter, handler, query_values)

    if state.verbose:
        typer.echo("Sending Request...")
    response = client.send_request(presenter, handler, body, path_dict, query_dict)
    print_response(response, state)

def path_list_to_dict(endpoint_resolver: EndpointResolver, presenter: str, handler: str, path_values: list[str]) -> dict[str, str]:
    # get param definitions
    path_params = endpoint_resolver.get_path_params(presenter, handler)

    # check if the number of provided params matches the definitions
    if len(path_params) < len(path_values):
        plural_s = "s" if len(path_params) > 1 else ''
        raise Exception(f"Expected {len(path_params)} PATH parameter{plural_s}, but got {len(path_values)}.")
    elif len(path_params) > len(path_values):
        missing_params = []
        for i in range(len(path_values), len(path_params)):
            missing_params.append(path_params[i]["python_name"])
        params_text = ", ".join(missing_params)
        plural_text = "s are" if len(missing_params) > 1 else ' is'
        raise Exception(f"The following PATH parameter{plural_text} missing: {params_text}.")

    # construct param_name->param_value dict
    path_dict = {}
    for i in range(len(path_params)):
        path_dict[path_params[i]["python_name"]] = path_values[i]
    return path_dict

def query_list_to_dict(endpoint_resolver: EndpointResolver, presenter: str, handler: str, query_values: list[str]) -> dict[str, str]:
    query_dict = {}
    for query_value in query_values:
        if query_value.count("=") != 1:
            raise Exception("The query values need to be in <name=value> format.")

        name, value = query_value.split("=")
        query_param = endpoint_resolver.get_query_param(presenter, handler, name)
        if not query_param or name != query_param["python_name"]:
            raise Exception(f"Unknown QUERY parameter: {name}.")

        # handle arrays
        if query_param["schema"]["type"] == "array":
            # arrays are delimited with commas
            value = value.split(",")
        
        query_dict[name] = value
    return query_dict

def prompt_endpoint(endpoint_resolver: EndpointResolver):
    presenter_choices = endpoint_resolver.get_presenters()
    question = [
        inquirer.List('presenter',
            message="What presenter would you like to use?",
            choices=presenter_choices,
        ),
    ]
    presenter = inquirer.prompt(question)['presenter']

    handler_choices = endpoint_resolver.get_handlers(presenter)
    question = [
        inquirer.List('handler',
            message="What handler would you like to use?",
            choices=handler_choices,
        ),
    ]
    handler = inquirer.prompt(question)['handler']

    return presenter, handler

def prompt_request_data(endpoint_resolver: EndpointResolver, presenter: str, handler: str):
    path_params = endpoint_resolver.get_path_params(presenter, handler)
    path_param_values = prompt_param_values(path_params)

    query_params = endpoint_resolver.get_query_params(presenter, handler)
    query_param_values = prompt_param_values(query_params)

    json_string = "{}"
    if endpoint_resolver.endpoint_has_body(presenter, handler):
        json_string = typer.prompt("Request Body [JSON]")

    return path_param_values, query_param_values, json_string

def prompt_param_values(params):
    param_values = {}
    for param in params:
        prompt_tokens = cmd_utils.get_param_info_text_tokens(param)
        prompt = " ".join(prompt_tokens.values())
        name = param["python_name"]
        required = param["required"]

        # get prompt value
        #TODO: handle lists
        if required:
            value = typer.prompt(prompt)
        else:
            value = typer.prompt(prompt, "", show_default=False)

        # do not propagate empty strings
        if value != "":
            param_values[name] = value

    return param_values

def help_callback(ctx: click.Context, _, display_help: bool):
    if not display_help:
        return display_help

    endpoint = ctx.params['endpoint']
    verbose = ctx.params['verbose']

    help_printer = HelpPrinter()
    help_printer.print(ctx, endpoint, verbose)
    return display_help
