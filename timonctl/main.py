from types import SimpleNamespace

import typer

from . import logger, settings
from .blueprint import app as app_blueprint
from .environment import app as app_environment


app = typer.Typer()
app.add_typer(app_blueprint, name="blueprint")
app.add_typer(app_environment, name="environment")


@app.command()
def login(ctx: typer.Context):
    logger.info(f"STUB: login with {ctx.obj.profile}")


@app.command()
def logout(ctx: typer.Context):
    logger.info(f"STUB: logout with {ctx.obj.profile}")


@app.callback()
def entrypoint(ctx: typer.Context,
               profile: str = typer.Option("default", envvar="TIMON_PROFILE")):

    project_id = settings.profiles.get(profile).project_id

    ctx.obj = SimpleNamespace(
        profile=profile,
        project_id=project_id
    )


# NOTE: this intermediate step is required to be able to add common
#       arguments with entrypoint()
#
#       https://jacobian.org/til/common-arguments-with-typer/
def main():
    app()


if __name__ == "__main__":
    main()
