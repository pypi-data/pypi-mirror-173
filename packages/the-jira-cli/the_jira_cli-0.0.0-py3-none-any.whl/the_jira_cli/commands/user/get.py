from the_jira_cli.config import *
import click
import the_jira_cli.cli
import json
import sys


@click.command("get", help="get or search for a user")
@click.option("--username", help="search for a user by username", type=str, required=False)
@click.option("--email", help="search for a user by email", type=str, required=False)
@click.option("--key", help="get a user by key", type=str, required=False)
@click.option("--account-id", help="get a user by account_id", type=str, required=False)
@click.option("--expand-application-roles", is_flag=True, help="expand the user's application roles", default=False)
@click.option("--expand-groups", is_flag=True, help="expand the user's groups", default=False)
def get_cmd(username, email, key, account_id, expand_application_roles, expand_groups):
    if cli.no_args():
        cli.print_help()
    expand = []
    if expand_application_roles:
        expand.append("applicationRoles")
    if expand_groups:
        expand.append("groups")
    if key:
        u = jira.user(key=key, expand=expand)
        print_user(u)
    if account_id:
        u = jira.user(account_id=account_id, expand=expand)
        print_user(u)
    if username and email:
        click.UsageError("Username and email cannot both be specified at once")
    if username is not None and username != "":
        u = jira.user_find_by_user_string(query=username)
        print_user(u)


def print_user(user: dict | list) -> None:
    if isinstance(user, list):
        if len(user) == 0:
            cli.echo_msg(msg="user not found")
        elif len(user) == 1:
            cli.echo_data(user[0])
        elif len(user) > 1:
            cli.echo_data(resolve(user))
    elif isinstance(user, dict):
        cli.echo_data(user)
    else:
        cli.echo_msg(msg="user not found")


def resolve(user):
    """Prints out a summary of the users found for the cli user to choose from
    This function writes all prompts to the user to stderr so that the json output
    of the cli is left intact for downstream consumers
    """
    click.echo("\nMultiple users found:\n", err=True)
    user_candidates = dict()
    i = 1

    TAB = "\t"
    sys.stderr.write(f"displayName{5*TAB}emailAddress\n")
    for u in user:
        user_key = f"{u.get('displayName')}{4*TAB}{u.get('emailAddress')}"
        sys.stderr.write(f"{i}: {user_key}\n")
        user_candidates.update({str(i): u})
        i += 1
    sys.stderr.write("\nEnter a number to select a user: ")
    selection = input()
    return user_candidates.get(str(selection))
