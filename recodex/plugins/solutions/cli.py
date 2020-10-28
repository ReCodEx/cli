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


@cli.command()
@click.argument("solution_id")
@click.argument("points", type=int)
@click.option('--override', '-o', type=int, default=None)
@pass_api_client
def set_bonus_points(api: ApiClient, solution_id, points, override):
    """
    Set bonus points and optionally also points override.
    """

    api.solution_set_bonus_points(solution_id, points, override)


@cli.command()
@click.argument("flag")
@click.argument("solution_id")
@click.option('--unset', is_flag=True)
@pass_api_client
def set_flag(api: ApiClient, flag, solution_id, unset):
    """
    Set solution flag (accepted or reviewed).
    """

    if flag not in ["accepted", "reviewed"]:
        click.echo("Invalid flag '{}'.".format(flag))
    else:
        api.solution_set_flag(solution_id, flag, not unset)


@cli.command()
@click.argument("solution_id")
@click.option('--debug', is_flag=True)
@pass_api_client
def resubmit(api: ApiClient, solution_id, debug):
    """
    Resubmit given solution for re-evaluation.
    """

    api.solution_resubmit(solution_id, debug)


@cli.command()
@click.argument("solution_id")
@pass_api_client
def delete(api: ApiClient, solution_id):
    """
    Delete solution, all related files, and all submission results.
    """

    api.delete_solution(solution_id)
