from tabulate import tabulate
import typer

from . import logger
from .api import Timon
from .exceptions import TimonApiException
from .models import *

app = typer.Typer()


@app.command("import")
def import_environment(ctx: typer.Context, name: str, repository: str = "timontech/environments", repository_server="https://github.com", project_id_or_name: str = typer.Option(default=None)):
    if project_id_or_name:
        pass
    elif ctx.obj.project_id:
        project_id = ctx.obj.project_id

    try:
        t = Timon(ctx.obj.profile)
        environment = t.import_environment(name, repository, repository_server, project_id)
        print(environment)
    except TimonApiException as e:
        logger.error(str(e))


@app.command("list")
def list_environment(ctx: typer.Context, project_id_or_name: str = typer.Option(default=None)):
    if project_id_or_name:
        pass
    elif ctx.obj.project_id:
        project_id = ctx.obj.project_id

    try:
        t = Timon(ctx.obj.profile)
        environments = t.get_environments(project_id)
        print(tabulate([x.dict().values() for x in environments], headers=Environment.get_field_names(), tablefmt="psql"))
    except TimonApiException as e:
        logger.error(str(e))


@app.command("show")
def show_environment(ctx: typer.Context, environment_id_or_name: str, project_id_or_name: str = typer.Option(default=None)):
    if project_id_or_name:
        pass
    elif ctx.obj.project_id:
        project_id = ctx.obj.project_id

    try:
        t = Timon(ctx.obj.profile)
        environment = t.get_environment(environment_id_or_name, project_id)
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
def delete_environment(ctx: typer.Context, environment_id_or_name: str, project_id_or_name: str = typer.Option(default=None)):
    if project_id_or_name:
        pass
    elif ctx.obj.project_id:
        project_id = ctx.obj.project_id

    try:
        t = Timon(ctx.obj.profile)
        result = t.delete_environment(environment_id_or_name, project_id)
        print(result)
    except TimonApiException as e:
        logger.error(str(e))
