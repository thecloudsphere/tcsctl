from tabulate import tabulate
import typer
import uuid as uuid_pkg

from . import logger
from .api import Timon
from .exceptions import TimonApiException
from .models import *

app = typer.Typer()


@app.command("import")
def import_environment(repository: str, name: str):
    logger.info("STUB: import_environment")


@app.command("list")
def list_environment(ctx: typer.Context, project_id: uuid_pkg.UUID):
    try:
        t = Timon(ctx.obj.profile)
        environments = t.get_environments(project_id)
        print(tabulate([x.dict().values() for x in environments], headers=Environment.get_field_names(), tablefmt="psql"))
    except TimonApiException as e:
        logger.error(str(e))


@app.command("show")
def show_environment(ctx: typer.Context, environment_id: uuid_pkg.UUID, project_id: uuid_pkg.UUID = typer.Option(default=None)):
    try:
        t = Timon(ctx.obj.profile)
        environment = t.get_environment(environment_id, project_id)
        print(environment)
    except TimonApiException as e:
        logger.error(str(e))


@app.command("edit")
def edit_environment(name: str):
    logger.info("STUB: edit_environment")


@app.command("update")
def update_environment(name: str):
    logger.info("STUB: update_environment")


@app.command("delete")
def delete_environment(name: str):
    logger.info("STUB: delete_environment")
