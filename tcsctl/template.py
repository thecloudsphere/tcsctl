from typing import List

from pandas import DataFrame
from tabulate import tabulate
import typer

from . import logger
from .exceptions import TimonApiException, TimonException
from .models import *


app = typer.Typer()


@app.command("import")
def import_template(ctx: typer.Context, path: str, name: str):
    try:
        template = ctx.obj.client.import_template(path, name, ctx.obj.project_id)
        print(tabulate(template, headers=["Field", "Value"], tablefmt="psql"))
    except TimonApiException as e:
        logger.error(str(e))
    except TimonException as e:
        print(str(e))


@app.command("list")
def list_templates(
    ctx: typer.Context,
    column: List[str] = typer.Option(
        default=[],
        help="Specify the column(s) to include, can be repeated to show multiple columns",
    ),
):
    try:
        templates = ctx.obj.client.get_templates(ctx.obj.project_id)
        df = DataFrame(
            (x.dict().values() for x in templates),
            columns=Template.get_field_names(),
        )
        if column:
            result = tabulate(df.filter(items=column), headers=column, tablefmt="psql")
        else:
            result = tabulate(
                df,
                headers=df.columns,
                tablefmt="psql",
            )

        print(result)
    except TimonApiException as e:
        logger.error(str(e))


@app.command("show")
def show_template(ctx: typer.Context, name: str):
    try:
        template = ctx.obj.client.get_template(name, ctx.obj.project_id)
        print(tabulate(template, headers=["Field", "Value"], tablefmt="psql"))
    except TimonApiException as e:
        logger.error(str(e))


@app.command("edit")
def edit_template(ctx: typer.Context, name: str):
    logger.info("STUB: edit_template")


@app.command("update")
def update_template(ctx: typer.Context, name: str):
    logger.info("STUB: update_template")


@app.command("delete")
def delete_template(ctx: typer.Context, name: str):
    try:
        ctx.obj.client.delete_template(name, ctx.obj.project_id)
        logger.info(f"Template {name} deleted")
    except TimonApiException as e:
        logger.error(str(e))
