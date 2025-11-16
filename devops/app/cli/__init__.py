import rich_click as click
from app.cli.env import env
from app.cli.user import user
from app.cli.service import service

@click.group()
def cli() -> None:
    pass

cli.add_command(env)
cli.add_command(user)
cli.add_command(service)