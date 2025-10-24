import click
from rich.console import Console
from rich.panel import Panel
from recodex.client_components.endpoint_resolver import EndpointResolver

from ..utils import cmd_utils as cmd_utils


class HelpPrinter:
    """Class handling detailed help messages for the call command endpoints.
    """

    path_panel: Panel | None = None
    query_panel: Panel | None = None
    body_panel: Panel | None = None
    console: Console | None = None

    def _add_text_token(
            self,
            texts: list[str],
            token_dicts: list[dict[str, str]],
            token_key: str,
            color: str = "white"
    ):
        max_len = 0
        for text in texts:
            if len(text) > max_len:
                max_len = len(text)

        for i in range(len(texts)):
            if token_key not in token_dicts[i]:
                continue
            # append texts with spaces
            texts[i] += " " * (max_len - len(texts[i]))
            # add token
            token = f" {token_dicts[i][token_key]}".replace("[", "\\[")
            # add token color
            token = f"[{color}]{token}[/{color}]"
            texts[i] += token

    def _create_panel(self, text: str, title: str) -> Panel:
        # escape opening brackets

        return Panel(
            text,
            border_style="dim",
            title=title,
            title_align="left",
        )

    def _prepare_param_table(self, rows_tokenized: list[dict]) -> str:
        rows = ["" for i in range(len(rows_tokenized))]
        self._add_text_token(rows, rows_tokenized, "name", "bright_cyan")
        self._add_text_token(rows, rows_tokenized, "type", "yellow")
        self._add_text_token(rows, rows_tokenized, "opt", "magenta")
        self._add_text_token(rows, rows_tokenized, "desc")
        return "\n".join(rows)

    def _get_param_panel(self, params: list[dict], title: str) -> Panel:
        rows_tokenized = []
        for param in params:
            rows_tokenized.append(cmd_utils.get_param_info_text_tokens(param))

        return self._create_panel(self._prepare_param_table(rows_tokenized), title)

    def _get_body_panel(self, body_schema: dict | None, body_types: list[str], title: str) -> Panel:
        if not body_types:
            body_types = ["[unknown]"]

        types_text = "[bright_black]A body is required of the following type(s):[/bright_black] " + ", ".join(
            body_types)
        if body_schema is None:
            return self._create_panel(types_text, title)

        types_text += "\n[bright_black]Body schema:[/bright_black]\n"
        rows_tokenized = cmd_utils.get_body_params_info_text_tokens(body_schema)
        return self._create_panel(types_text + self._prepare_param_table(rows_tokenized), title)

    def _prepare(self, ctx: click.Context, endpoint: str, verbose: bool):
        self.ctx = ctx
        self.formatter = ctx.make_formatter()

        self.print_detail = endpoint != ""
        if self.print_detail:
            def __init():
                self.presenter, self.action = cmd_utils.execute_with_verbosity(
                    lambda: cmd_utils.parse_endpoint_or_throw(endpoint),
                    verbose
                )
                endpoint_resolver = EndpointResolver()
                self.console = Console()
                path_params = endpoint_resolver.get_path_params(self.presenter, self.action)
                query_params = endpoint_resolver.get_query_params(self.presenter, self.action)
                body_schema = endpoint_resolver.get_request_body_schema(self.presenter, self.action)
                body_types = endpoint_resolver.get_request_body_types(self.presenter, self.action)

                self.description = endpoint_resolver.get_endpoint_description(self.presenter, self.action)
                self.path_panel, self.query_panel, self.body_panel = None, None, None
                if len(path_params) > 0:
                    self.path_panel = self._get_param_panel(path_params, "Path Parameters Detail")
                if len(query_params) > 0:
                    self.query_panel = self._get_param_panel(query_params, "Query Parameters Detail")
                if endpoint_resolver.endpoint_has_body(self.presenter, self.action):
                    self.body_panel = self._get_body_panel(body_schema, body_types, "Body Detail")
            cmd_utils.execute_with_verbosity(__init, verbose)

    def print(self, ctx: click.Context, endpoint: str, verbose: bool):
        self._prepare(ctx, endpoint, verbose)
        self.ctx.command.format_help(self.ctx, self.formatter)

        if self.print_detail:
            if self.console is None:
                raise Exception("The Console was not instantiated properly.")
            self.console.print("\n[bold]Endpoint Detail[/bold]:")
            self.console.print(f"Presenter: [yellow]{self.presenter}[/yellow]")
            self.console.print(f"Action: [yellow]{self.action}[/yellow]")
            self.console.print(f"Description: [bright_black]{self.description}[/bright_black]\n")

            if self.path_panel:
                self.console.print(self.path_panel)
            if self.query_panel:
                self.console.print(self.query_panel)
            if self.body_panel:
                self.console.print(self.body_panel)
