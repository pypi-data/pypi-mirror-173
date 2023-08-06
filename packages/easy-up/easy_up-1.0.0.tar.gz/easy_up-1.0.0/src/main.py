import click
import sys
from .utils import get_sys_info
from .github import Github


@click.group('Update Tool')
def cli():
    if get_sys_info().system.lower() != 'windows':
        click.secho('PackageManager Not Support your OS Now.')
        sys.exit(1)


@cli.command()
@click.option('-l', '--repo-url', help='Github Repository Path {OWNER}/{REPO_NAME}')
@click.option('--ext', help='Select Custom Extension')
def github(repo_url, ext):
    if repo_url:
        update = Github(url=repo_url)
        update.ext = ext if ext is not None else None
        update.install()
        sys.exit(0)
    sys.stdout.write('Hello, Update Manager')


if __name__ == '__main__':
    cli()
