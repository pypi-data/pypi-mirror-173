import click


@click.group(name="sprint", help="Manage sprints")
def sprint_cmd():
    raise click.UsageError("This command hasn't been implemented yet")
