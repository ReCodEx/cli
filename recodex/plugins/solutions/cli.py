import click

from recodex.api import ApiClient
from recodex.decorators import pass_api_client


@click.group()
def cli():
    """
    Tools for working with (assignment) solutions
    """


@cli.command()
@click.argument("solution_id")
@click.argument("download_as")
@pass_api_client
def download(api: ApiClient, solution_id, download_as):
    """
    Download files of given solution in a ZIP archive.
    """

    api.download_solution(solution_id, download_as)
