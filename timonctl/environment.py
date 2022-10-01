from tabulate import tabulate
import typer

from . import logger
from .exceptions import TimonApiException
from .models import *

app = typer.Typer()


@app.command("import")
def import_environment(ctx: typer.Context, name: str, repository: str = "timontech/registry", repository_server="https://github.com", project: str = typer.Option(default=None)):
    try:
        environment = ctx.obj.client.import_environment(name, repository, "environments", repository_server, project)
        print(environment)
    except TimonApiException as e:
        logger.error(str(e))


@app.command("list")
def list_environment(ctx: typer.Context, project: str = typer.Option(default=None)):
    try:
        environments = ctx.obj.client.get_environments(project)
        print(tabulate([x.dict().values() for x in environments], headers=Environment.get_field_names(), tablefmt="psql"))
    except TimonApiException as e:
        logger.error(str(e))


@app.command("show")
def show_environment(ctx: typer.Context, name: str, project: str = typer.Option(default=None)):
    try:
        environment = ctx.obj.client.get_environment(name, project)
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
def delete_environment(ctx: typer.Context, name: str, project: str = typer.Option(default=None)):
    try:
        result = ctx.obj.client.delete_environment(name, project)
        print(result)
    except TimonApiException as e:
        logger.error(str(e))
