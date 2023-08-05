import os, sys
import logging
import pathlib
import requests

from .utils import console_handler, abort
from . import app

log = logging.getLogger(__name__)
help_string = """A utility for managing Unknown projects"""

base_path = pathlib.Path(os.path.dirname(__file__))
commands_folder = base_path / "commands"

from typer import Typer, Context, Argument, Option, echo, secho, confirm

@app.callback(context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def cli(
    ctx: Context,
    verbose: str = Option(None, "-v", "--verbose", help="Verbose logging: info or debug"),
    profile: str = Option(None, "-p", "--profile", help="Profile name if you want to override the default profile"),
    output: str = Option("text", "-o", "--output", help="Output text or json"),
    tenant: str = Option(None, "-t", "--tenant", help="Override the tenant for this command"),
    domain: str = Option(None, "-d", "--domain", help="Override the domain for this command"),
):
    # by default we log out to console WARN and higher but can view info with -v
    # make sure this is called before importing the sdk so that we can grab all logging
    if verbose:
        console_handler.setLevel(getattr(logging, verbose.upper()))


from unknowncli.commands import project

app.add_typer(project.app, name="project", help="Manage project setup")
