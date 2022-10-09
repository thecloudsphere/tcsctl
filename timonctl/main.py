from getpass import getpass
import os
import sys
from types import SimpleNamespace

from tabulate import tabulate
import typer

from . import logger, settings, user_config_dir
from .api import get_client, get_http_client
from .blueprint import app as app_blueprint
from .common import get_token_from_file
from .deployment import app as app_deployment
from .environment import app as app_environment
from .exceptions import TimonApiException
from .project import app as app_project
from .template import app as app_template


app = typer.Typer()
app.add_typer(app_blueprint, name="blueprint")
app.add_typer(app_deployment, name="deployment")
app.add_typer(app_environment, name="environment")
app.add_typer(app_project, name="project")
app.add_typer(app_template, name="template")


@app.command()
def login(ctx: typer.Context, force: bool = typer.Option(False, "--force"), prompt: bool = typer.Option(False, "--prompt"), show: bool = typer.Option(False, "--show")):
    token = None

    if not force:
        token = get_token_from_file(ctx.obj.profile.name)

    if not token:
        password = None
        if force:
            ctx.obj.profile.auth.password = getpass()
        else:
            password = ctx.obj.profile.auth.get("password")
        if not password:
            ctx.obj.profile.auth.password = getpass()

        client = get_http_client(ctx.obj.profile)
        logger.debug(f"Requesting new token for {ctx.obj.profile.name}")
        token = client.login()
        print("Logged in successfully.")
    else:
        print("Already logged in.")

    if show:
        print(tabulate(token, headers=["Field", "Value"], tablefmt="psql"))


@app.command()
def logout(ctx: typer.Context):
    path = os.path.join(user_config_dir(), f"{ctx.obj.profile.name}.json")
    logger.debug(f"Removing token for {ctx.obj.profile.name}: {path}")
    try:
        os.remove(path)
        print("Logged out successfully.")
    except FileNotFoundError:
        print("Already logged out.")


@app.callback()
def entrypoint(ctx: typer.Context,
               profile: str = typer.Option("default", envvar="TIMON_PROFILE")):

    ns_profile = settings.profiles.get(profile)
    ns_profile.name = profile

    if ctx.invoked_subcommand not in ["login", "logout"]:
        try:
            client = get_client(ns_profile)
        except TimonApiException as e:
            logger.error(str(e))
            sys.exit(1)

        ctx.obj = SimpleNamespace(
            client=client,
            organisation_id=client.organisation_id,
            profile=ns_profile,
            project_id=client.project_id
        )
    else:
        ctx.obj = SimpleNamespace(
            profile=ns_profile
        )


# NOTE: this intermediate step is required to be able to add common
#       arguments with entrypoint()
#
#       https://jacobian.org/til/common-arguments-with-typer/
def main():
    app()


if __name__ == "__main__":
    main()
