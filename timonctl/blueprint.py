from tabulate import tabulate
import typer

from . import logger
from .api import Timon
from .exceptions import TimonApiException
from .models import *


app = typer.Typer()


@app.command("import")
def import_blueprint(ctx: typer.Context, name: str, repository: str = "timontech/blueprints", repository_server="https://github.com", project_id_or_name: str = typer.Option(default=None)):
    if project_id_or_name:
        pass
    elif ctx.obj.project_id:
        project_id = ctx.obj.project_id

    try:
        t = Timon(ctx.obj.profile)
        blueprint = t.import_blueprint(name, repository, repository_server, project_id)
        print(blueprint)
    except TimonApiException as e:
        logger.error(str(e))


@app.command("list")
def list_blueprints(ctx: typer.Context, project_id_or_name: str = typer.Option(default=None)):
    if project_id_or_name:
        pass
    elif ctx.obj.project_id:
        project_id = ctx.obj.project_id

    try:
        t = Timon(ctx.obj.profile)
        blueprints = t.get_blueprints(project_id)
        print(tabulate([x.dict().values() for x in blueprints], headers=Blueprint.get_field_names(), tablefmt="psql"))
    except TimonApiException as e:
        logger.error(str(e))


@app.command("show")
def show_blueprint(ctx: typer.Context, blueprint_id_or_name: str, project_id_or_name: str = typer.Option(default=None)):
    if project_id_or_name:
        pass
    elif ctx.obj.project_id:
        project_id = ctx.obj.project_id

    try:
        t = Timon(ctx.obj.profile)
        blueprint = t.get_blueprint(blueprint_id_or_name, project_id)
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
def delete_blueprint(ctx: typer.Context, blueprint_id_or_name: str, project_id_or_name: str = typer.Option(default=None)):
    if project_id_or_name:
        pass
    elif ctx.obj.project_id:
        project_id = ctx.obj.project_id

    try:
        t = Timon(ctx.obj.profile)
        result = t.delete_blueprint(blueprint_id_or_name, project_id)
        print(result)
    except TimonApiException as e:
        logger.error(str(e))
