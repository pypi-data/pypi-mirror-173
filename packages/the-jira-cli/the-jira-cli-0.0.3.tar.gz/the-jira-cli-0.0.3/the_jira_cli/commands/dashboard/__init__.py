import click


@click.group(name="dashboard", help="Manage dashboards")
def dashboard_cmd():
    raise click.UsageError("This command hasn't been implemented yet")
