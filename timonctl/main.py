from types import SimpleNamespace

import typer

from . import logger
from .api import get_api_client
from .blueprint import app as app_blueprint
from .deployment import app as app_deployment
from .environment import app as app_environment
from .template import app as app_template


app = typer.Typer()
app.add_typer(app_blueprint, name="blueprint")
app.add_typer(app_deployment, name="deployment")
app.add_typer(app_environment, name="environment")
app.add_typer(app_template, name="template")


@app.command()
def login(ctx: typer.Context):
    logger.info(f"STUB: login with {ctx.obj.profile}")


@app.command()
def logout(ctx: typer.Context):
    logger.info(f"STUB: logout with {ctx.obj.profile}")


@app.callback()
def entrypoint(ctx: typer.Context,
               profile: str = typer.Option("default", envvar="TIMON_PROFILE")):

    client = get_api_client(profile)

    ctx.obj = SimpleNamespace(
        client=client,
        organisationd_id=client.organisation_id,
        profile=profile,
        project_id=client.project_id
    )


# NOTE: this intermediate step is required to be able to add common
#       arguments with entrypoint()
#
#       https://jacobian.org/til/common-arguments-with-typer/
def main():
    app()


if __name__ == "__main__":
    main()
