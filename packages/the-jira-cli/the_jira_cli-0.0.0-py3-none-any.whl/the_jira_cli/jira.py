import click

from .commands import command_groups


@click.group()
def jira():
    pass


for command in command_groups:
    jira.add_command(command, command.name)

if __name__ == "__main__":
    jira()
