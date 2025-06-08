import call_command.cmd_utils as cmd_utils

class CommandState:
  # whether debug error messages should be shown
  verbose: bool = False

  # what format should be used for the output (json or yaml)
  output_format = "json"

  # if set, the output will be saved to the path
  output_path: str|None = None

  # whether the output should be minimized
  output_minimized: bool = False
