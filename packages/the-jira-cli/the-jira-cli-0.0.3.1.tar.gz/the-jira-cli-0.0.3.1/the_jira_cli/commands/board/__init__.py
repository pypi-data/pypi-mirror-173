import click


@click.group(name="board", help="Manage boards")
def board_cmd():
    raise click.UsageError("This command hasn't been implemented yet")
