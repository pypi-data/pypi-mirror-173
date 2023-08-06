import click


@click.group(name="audit-record", help="Manage audit records")
def audit_record_cmd():
    raise click.UsageError("This command hasn't been implemented yet")
