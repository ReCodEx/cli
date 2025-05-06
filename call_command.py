from recodex_cli_lib import client_factory
from recodex_cli_lib.endpoint_resolver import EndpointResolver
from recodex_cli_lib.client import Client
import typer
import json
import inquirer

def parse_json(json_string):
    try:
        return json.loads(json_string)
    except:
        raise Exception("The JSON string is corrupted.")

def call_interactive(client: Client):
    # start an interactive prompt if there is no endpoint
    endpoint_resolver = EndpointResolver()
    presenter, handler = prompt_endpoint(endpoint_resolver)
    endpoint = f"{presenter}.{handler}"
    path_param_values, query_param_values, body_string = prompt_request_data(endpoint_resolver, presenter, handler)
    body = parse_json(body_string)
    
    call(client, endpoint, path_param_values, query_param_values, body)

def call(client: Client, endpoint: str, path_param_values: dict[str, str], query_param_values: dict[str, str], body: dict):
    if endpoint.count(".") != 1:
        raise Exception("The endpoint needs to be in <presenter.handler> format.")

    presenter, handler = endpoint.split(".")
    response = client.send_request(presenter, handler, body, path_param_values, query_param_values)
    print(response.headers)

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
        # get prompt info
        name = param["name"]
        desc = param["description"]
        type = param["schema"]["type"]
        if param["schema"]["nullable"]:
            type += "|null"
        required = param["required"]

        # construct prompt
        prompt = f"{name} [{type}]"
        if not required:
            prompt += f" [OPT]"
        prompt += f" ({desc})"

        # get prompt value
        #TODO: handle lists
        value = typer.prompt(prompt)
        while required and value == "":
            value = typer.prompt(prompt)

        # do not propagate empty strings
        if value != "":
            param_values[name] = value

    return param_values

    