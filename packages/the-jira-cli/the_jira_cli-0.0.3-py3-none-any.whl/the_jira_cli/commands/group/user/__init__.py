import click


@click.group(name="user", help="Manage users in a group")
def user_cmd():
    raise click.UsageError("This command hasn't been implemented yet")
