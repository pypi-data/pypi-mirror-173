import click


@click.group(name="component", help="Manage components")
def component_cmd():
    raise click.UsageError("This command hasn't been implemented yet")
