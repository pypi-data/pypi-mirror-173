import click
from .user import user_cmd

@click.group(name="group", help="Manage groups")
def group_cmd():
    raise click.UsageError("This command hasn't been implemented yet")

group_cmd.add_command(user_cmd)