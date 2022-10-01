from tabulate import tabulate
import typer

from . import logger
from .exceptions import TimonApiException
from .models import *

app = typer.Typer()


@app.command("list")
def list_deployment(ctx: typer.Context, project: str = typer.Option(default=None)):
    try:
        deployments = ctx.obj.client.get_deployments(project)
        print(tabulate([x.dict().values() for x in deployments], headers=Deployment.get_field_names(), tablefmt="psql"))
    except TimonApiException as e:
        logger.error(str(e))


@app.command("create")
def create_deployment(ctx: typer.Context, name: str, template: str, project: str = typer.Option(default=None)):
    try:
        deployment = ctx.obj.client.create_deployment(name, template, project)
        print(tabulate(deployment, headers=["Field", "Value"], tablefmt="psql"))
    except TimonApiException as e:
        logger.error(str(e))


@app.command("destroy")
def destroy_deployment(ctx: typer.Context, name: str, project: str = typer.Option(default=None)):
    try:
        result = ctx.obj.client.destroy_deployment(name, project)
        print(result)
    except TimonApiException as e:
        logger.error(str(e))


@app.command("show")
def show_deployment(ctx: typer.Context, name: str, project: str = typer.Option(default=None)):
    try:
        deployment = ctx.obj.client.get_deployment(name, project)
        print(tabulate(deployment, headers=["Field", "Value"], tablefmt="psql"))
    except TimonApiException as e:
        logger.error(str(e))


@app.command("edit")
def edit_deployment(name: str):
    logger.info("STUB: edit_deployment")


@app.command("update")
def update_deployment(name: str):
    logger.info("STUB: update_deployment")


@app.command("delete")
def delete_deployment(ctx: typer.Context, name: str, project: str = typer.Option(default=None)):
    try:
        result = ctx.obj.client.delete_deployment(name, project)
        print(result)
    except TimonApiException as e:
        logger.error(str(e))
