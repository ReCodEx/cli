from recodex_cli_lib import client_factory
from recodex_cli_lib.endpoint_resolver import EndpointResolver
from recodex_cli_lib.client import Client
import typer
import json
import inquirer
from rich.console import Console
from rich.panel import Panel

def parse_json(json_string):
    try:
        return json.loads(json_string)
    except:
        raise Exception("The JSON string is corrupted.")

def call_interactive(client: Client, verbose: bool):
    # start an interactive prompt if there is no endpoint
    endpoint_resolver = EndpointResolver()
    presenter, handler = prompt_endpoint(endpoint_resolver)
    endpoint = f"{presenter}.{handler}"
    path_param_values, query_param_values, body_string = prompt_request_data(endpoint_resolver, presenter, handler)
    body = parse_json(body_string)
    
    call(client, endpoint, path_param_values, query_param_values, body, verbose)

def call(client: Client, endpoint: str, path_param_values: dict[str, str], query_param_values: dict[str, str], body: dict, verbose: bool):
    presenter, handler = parse_endpoint_or_throw(endpoint)
    if verbose:
        typer.echo("Sending Request...")
    response = client.send_request(presenter, handler, body, path_param_values, query_param_values)
    print(response.headers)

def parse_endpoint_or_throw(endpoint: str):
    if endpoint.count(".") != 1:
        raise Exception("The endpoint needs to be in <presenter.handler> format.")

    presenter, handler = endpoint.split(".")
    return presenter, handler

def print_help_for_endpoint(endpoint: str):
    #TODO: handle no endpoint specified help
    presenter, handler = parse_endpoint_or_throw(endpoint)
    endpoint_resolver = EndpointResolver()
    console = Console()

    path_params = endpoint_resolver.get_path_params(presenter, handler)
    if (len(path_params) > 0):
        console.print(get_param_panel(path_params, "Path Parameters"))

    query_params = endpoint_resolver.get_query_params(presenter, handler)
    if (len(query_params) > 0):
        console.print(get_param_panel(query_params, "Query Parameters"))

    if endpoint_resolver.endpoint_has_body(presenter, handler):
        console.print(create_panel("The endpoint expects a JSON body.", "Body"))

def get_param_panel(params: list[dict], title):
    rows_tokenized = []
    for param in params:
        rows_tokenized.append(get_param_info_text_tokens(param))

    rows = ["" for i in range(len(rows_tokenized))]

    __add_text_token(rows, rows_tokenized, "name")
    __add_text_token(rows, rows_tokenized, "type")
    __add_text_token(rows, rows_tokenized, "opt")
    __add_text_token(rows, rows_tokenized, "desc")

    text = "\n".join(rows)
    return create_panel(text, title)

def __add_text_token(texts: list[str], token_dicts: list[dict[str, str]], token_key: str):
    max_len = 0
    for text in texts:
        if len(text) > max_len:
            max_len = len(text)

    for i in range(len(texts)):
        # append texts with spaces
        texts[i] += " " * (max_len - len(texts[i]))
        # add token
        texts[i] += f" {token_dicts[i][token_key]}"


def create_panel(text: str, title: str):
        # escape opening brackets
        text = text.replace("[", "\[")

        return Panel(
        text,
        border_style="dim",
        title=title,
        title_align="left",
    )

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

def get_param_info_text_tokens(param: dict):
    # get info
    name = param["name"]
    desc = param["description"]
    type = param["schema"]["type"]
    if param["schema"]["nullable"]:
        type += "|null"
    required = param["required"]

    tokens = {
        "name": name,
        "type": f"[{type}]",
    }
    if not required:
        tokens["opt"] = "[OPT]"
    tokens["desc"] = desc

    return tokens

def prompt_param_values(params):
    param_values = {}
    for param in params:
        prompt_tokens = get_param_info_text_tokens(param)
        prompt = " ".join(prompt_tokens.values())
        name = param["name"]
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

    