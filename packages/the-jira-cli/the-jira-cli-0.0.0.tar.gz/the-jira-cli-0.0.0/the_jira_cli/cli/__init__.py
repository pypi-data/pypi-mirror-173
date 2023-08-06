import click
import inspect
import json


def no_args() -> bool:
    """ Checks whether no arguments were passed to the command
    Uses inspect to examine the local variables of the caller
    Kudos to: https://stackoverflow.com/a/6618825
    """
    frame = inspect.currentframe()
    try:
        return not any([
            a is not None
            and a != ""
            and a != False
            for a in frame.f_back.f_locals.values()
        ])
    finally:
        del frame


def print_help():
    """ Prints the help message for the current command
    """
    ctx = click.get_current_context()
    click.echo(ctx.get_help())
    ctx.exit()


def echo_msg(msg: str, **kwargs: dict) -> None:
    """ Formats a json message indicating the operation was not successful
    """
    d = {"message": msg}
    d.update(kwargs)
    click.echo(json.dumps(d))


def echo_data(data: dict, **kwargs: dict) -> None:
    """ Formats a json message with the data returned
    """
    if not isinstance(data, dict):
        data = {"data": data}
    data.update(kwargs)
    click.echo(json.dumps(data))
