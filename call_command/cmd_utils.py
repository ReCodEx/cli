import json
import click
import typing
from collections.abc import Callable

def parse_endpoint_or_throw(endpoint: str):
    if endpoint.count(".") != 1:
        raise Exception("The endpoint needs to be in <presenter.handler> format.")

    presenter, handler = endpoint.split(".")
    return presenter, handler

def parse_json(json_string):
    try:
        return json.loads(json_string)
    except:
        raise Exception("The JSON string is corrupted.")

def execute_with_verbosity(command: Callable[[], typing.Any], verbose: bool):
    try:
        return command()
    except Exception as e:
        if verbose:
            raise e
        else:
            raise click.ClickException(str(e))

def get_param_info_text_tokens(param: dict):
    # get info
    name = param["python_name"]
    desc = param["description"]
    type = param["schema"]["type"]
    if param["schema"]["nullable"]:
        type += "|null"
    required = param["required"]

    tokens = {
        "python_name": name,
        "type": f"[{type}]",
    }
    if not required:
        tokens["opt"] = "[OPT]"
    tokens["desc"] = desc

    return tokens
