from recodex_cli_lib.client_response import ClientResponse
from call_command.command_state import CommandState

def print_response(response: ClientResponse, state: CommandState):
  # get response string
  if state.output_format == "json":
    out_string = response.get_json_string(state.output_minimized)
  elif state.output_format == "yaml":
    out_string = response.get_yaml_string(state.output_minimized)
  else:
    raise NotImplementedError(f"Unknown output format '{state.output_format}'. Please use 'yaml' or 'json'.")
  
  # print to console or file
  if state.output_path == None:
    print(out_string)
  else:
    with open(state.output_path, "w") as handle:
      handle.write(out_string)
  