from tabulate import tabulate
import typer

from . import logger
from .exceptions import TimonApiException
from .models import *


app = typer.Typer()


@app.command("import")
def import_blueprint(ctx: typer.Context, name: str, repository: str = "timontech/registry", repository_server="https://github.com", project: str = typer.Option(default=None)):
    try:
        blueprint = ctx.obj.client.import_blueprint(name, repository, "blueprints", repository_server, project)
        print(blueprint)
    except TimonApiException as e:
        logger.error(str(e))


@app.command("list")
def list_blueprints(ctx: typer.Context, project: str = typer.Option(default=None)):
    try:
        blueprints = ctx.obj.client.get_blueprints(project)
        print(tabulate([x.dict().values() for x in blueprints], headers=Blueprint.get_field_names(), tablefmt="psql"))
    except TimonApiException as e:
        logger.error(str(e))


@app.command("show")
def show_blueprint(ctx: typer.Context, name: str, project: str = typer.Option(default=None)):
    try:
        blueprint = ctx.obj.client.get_blueprint(name, project)
        print(blueprint)
    except TimonApiException as e:
        logger.error(str(e))


@app.command("edit")
def edit_blueprint(ctx: typer.Context, name: str):
    logger.info("STUB: edit_blueprint")


@app.command("update")
def update_blueprint(ctx: typer.Context, name: str):
    logger.info("STUB: update_blueprint")


@app.command("delete")
def delete_blueprint(ctx: typer.Context, name: str, project: str = typer.Option(default=None)):
    try:
        result = ctx.obj.client.delete_blueprint(name, project)
        print(result)
    except TimonApiException as e:
        logger.error(str(e))
