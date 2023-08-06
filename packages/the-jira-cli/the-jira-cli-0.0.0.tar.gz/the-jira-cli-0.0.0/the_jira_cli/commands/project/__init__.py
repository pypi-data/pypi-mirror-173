import click
from .permission import permission_cmd


@click.group(name="project", help="Manage projects")
def project_cmd():
    raise click.UsageError("This command hasn't been implemented yet")


project_cmd.add_command(permission_cmd)
