from tabulate import tabulate
import typer
import uuid as uuid_pkg

from . import logger
from .api import Timon
from .exceptions import TimonApiException
from .models import *


app = typer.Typer()


@app.command("import")
def import_blueprint(repository: str, name: str):
    logger.info("STUB: import_blueprint")


@app.command("list")
def list_blueprints(ctx: typer.Context, project_id: uuid_pkg.UUID):
    try:
        t = Timon(ctx.obj.profile)
        blueprints = t.get_blueprints(project_id)
        print(tabulate([x.dict().values() for x in blueprints], headers=Blueprint.get_field_names(), tablefmt="psql"))
    except TimonApiException as e:
        logger.error(str(e))


@app.command("show")
def show_blueprint(ctx: typer.Context, blueprint_id: uuid_pkg.UUID, project_id: uuid_pkg.UUID = typer.Option(default=None)):
    try:
        t = Timon(ctx.obj.profile)
        blueprint = t.get_blueprint(blueprint_id, project_id)
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
def delete_blueprint(ctx: typer.Context, name: str):
    logger.info("STUB: delete_blueprint")
