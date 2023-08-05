import os, sys
import logging
import pathlib
import requests

from .utils import console_handler, abort

log = logging.getLogger(__name__)
help_string = """A utility for interfacing with Kamo dude"""

base_path = pathlib.Path(os.path.dirname(__file__))
commands_folder = base_path / "commands"

from typer import Typer, Context, Argument, Option, echo, secho, confirm

app = Typer()


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

    if ctx.obj is None:
        ctx.obj = ContextObj()
        ctx.obj.verbose = verbose
        ctx.obj.output = output
        try:
            ctx.obj.session = ServiceSession(profile=profile, tenant=tenant, domain=domain)
        except InvalidProfile as ex:
            log.debug(ex)
    try:
        out(
            f"Tenant: {ctx.obj.session.profile.tenant} - Profile: {ctx.obj.session.profile_name} - Endpoint: {ctx.obj.session.profile.domain}"
        )
    except:
        pass
    if ctx.invoked_subcommand not in ["tenants", "profile"]:
        if not ctx.obj.session:
            abort(f"You must create a profile with 'kamo profile add' to use this tool")

        if ctx.invoked_subcommand not in ["version"]:
            if not ctx.obj.session.profile.tenant:
                abort(f"You must select a tenant with 'kamo tenants' to use this tool")



from unknowncli.commands import p4setup

app.add_typer(p4setup.app, name="p4setup", help="Manage project setup")
