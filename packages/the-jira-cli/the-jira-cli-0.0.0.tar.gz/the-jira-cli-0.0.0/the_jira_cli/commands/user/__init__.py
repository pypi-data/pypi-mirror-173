import click
from .avatar import avatar_cmd
from .group import group_cmd
from .get import get_cmd


@click.group(name="user", help="Manage users")
def user_cmd():
    pass

user_cmd.add_command(avatar_cmd)
user_cmd.add_command(group_cmd)
user_cmd.add_command(get_cmd)
