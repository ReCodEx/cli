class CommandState:
    # whether debug error messages should be shown
    verbose: bool = False

    # what format should be used for the output (json, yaml, or raw)
    output_format = "json"

    # if set, the output will be saved to the path
    output_path: str | None = None

    # whether the output should be minimized (single-line json, minimized YAML)
    output_minimized: bool = False

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
