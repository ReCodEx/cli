import click
import sys
import json
from ruamel import yaml
import datetime

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


@cli.command()
@click.argument("solution_id")
@click.option("--json/--yaml", "useJson", default=None)
@pass_api_client
def get_comments(api: ApiClient, solution_id, useJson):
    """
    Get solution comments.
    """

    comments = api.get_solution_comments(solution_id)

    if useJson is True:
        json.dump(comments["comments"], sys.stdout, sort_keys=True, indent=4)
    elif useJson is False:
        yaml.dump(comments["comments"], sys.stdout)
    else:
        for comment in comments["comments"]:
            posted = datetime.datetime.fromtimestamp(comment["postedAt"]).strftime('%Y-%m-%d %H:%M:%S')
            click.echo("\n>>> {} at {} ({}) [{}]:".format(comment["user"]["name"], posted, "private" if comment["isPrivate"] else "public", comment["id"]))
            click.echo(comment["text"])
            click.echo("\n-----")
