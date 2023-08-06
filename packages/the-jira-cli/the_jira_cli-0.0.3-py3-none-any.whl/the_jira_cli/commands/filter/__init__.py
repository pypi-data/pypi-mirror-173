import click


@click.group(name="filter", help="Manage filters")
def filter_cmd():
    raise click.UsageError("This command hasn't been implemented yet")
