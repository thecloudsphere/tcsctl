from tabulate import tabulate
import typer

from . import logger
from .exceptions import TimonApiException
from .models import *


app = typer.Typer()


@app.command("import")
def import_template(ctx: typer.Context, path: str, name: str, project: str = typer.Option(default=None)):
    try:
        template = ctx.obj.client.import_template(path, name, project)
        print(template)
    except TimonApiException as e:
        logger.error(str(e))


@app.command("list")
def list_templates(ctx: typer.Context, project: str = typer.Option(default=None)):
    try:
        templates = ctx.obj.client.get_templates(project)
        print(tabulate([x.dict().values() for x in templates], headers=Template.get_field_names(), tablefmt="psql"))
    except TimonApiException as e:
        logger.error(str(e))


@app.command("show")
def show_template(ctx: typer.Context):
    logger.info("STUB: show_template")


@app.command("edit")
def edit_template(ctx: typer.Context, name: str):
    logger.info("STUB: edit_template")


@app.command("update")
def update_template(ctx: typer.Context, name: str):
    logger.info("STUB: update_template")


@app.command("delete")
def delete_template(ctx: typer.Context, name: str, project: str = typer.Option(default=None)):
    try:
        result = ctx.obj.client.delete_template(name, project)
        print(result)
    except TimonApiException as e:
        logger.error(str(e))
