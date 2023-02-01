import os
import subprocess
import tempfile
from types import SimpleNamespace
from typing import List

import jinja2
import json
from pandas import DataFrame
from tabulate import tabulate
import typer

from . import logger
from .common import is_valid_uuid
from .enums import DeploymentStatus
from .exceptions import TimonApiException
from .models import *

app = typer.Typer()


@app.command("list")
def list_deployment(
    ctx: typer.Context,
    column: List[str] = typer.Option(
        default=[],
        help="Specify the column(s) to include, can be repeated to show multiple columns",
    ),
):
    try:
        deployments = ctx.obj.client.get_deployments(ctx.obj.project_id)
        df = DataFrame(
            (x.dict().values() for x in deployments),
            columns=Deployment.get_field_names(),
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


@app.command("create")
def create_deployment(ctx: typer.Context, name: str, template: str):
    try:
        deployment = ctx.obj.client.create_deployment(
            name, template, ctx.obj.project_id
        )
        print(tabulate(deployment, headers=["Field", "Value"], tablefmt="psql"))
    except TimonApiException as e:
        logger.error(str(e))


@app.command("destroy")
def destroy_deployment(ctx: typer.Context, name: str):
    try:
        ctx.obj.client.destroy_deployment(name, ctx.obj.project_id)
        logger.info(f"Destroy of deployment {name} initiated")
    except TimonApiException as e:
        logger.error(str(e))


@app.command("reconcile")
def reconcile_deployment(ctx: typer.Context, name: str):
    try:
        ctx.obj.client.reconcile_deployment(name, ctx.obj.project_id)
        logger.info(f"Reconcile of deployment {name} initiated")
    except TimonApiException as e:
        logger.error(str(e))


@app.command("show")
def show_deployment(ctx: typer.Context, name: str):
    try:
        deployment = ctx.obj.client.get_deployment(name, ctx.obj.project_id)
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
def delete_deployment(ctx: typer.Context, name: str):
    try:
        ctx.obj.client.delete_deployment(name, ctx.obj.project_id)
        logger.info(f"Deployment {name} deleted")
    except TimonApiException as e:
        logger.error(str(e))


@app.command("outputs")
def get_deployment_outputs(
    ctx: typer.Context,
    name: str,
    output: str = typer.Argument(default=None),
    file: str = typer.Option(default=None, help="Write to file instead of stdout"),
):
    try:
        outputs = ctx.obj.client.get_deployment_outputs(
            name, output, ctx.obj.project_id
        )
        if output:
            result = outputs[output]
        else:
            result = outputs

        if file:
            with open(file, "w+") as fp:
                print(
                    f"Output {output} from deployment {name} was written to file {file}."
                )
                fp.write(result)
        else:
            print(result)
    except TimonApiException as e:
        logger.error(str(e))


@app.command("logs")
def get_deployment_logs(
    ctx: typer.Context,
    name: str,
    log_filter: str = typer.Argument(default="1 hour ago"),
    show: bool = typer.Option(default=False),
):
    try:
        if is_valid_uuid(log_filter):
            log = ctx.obj.client.get_deployment_log(
                name, log_filter, ctx.obj.project_id
            )
            print(log.value)
        else:
            logs = ctx.obj.client.get_deployment_logs(
                name, ctx.obj.project_id, log_filter
            )
            if show:
                for log in logs:
                    log_with_value = ctx.obj.client.get_deployment_log(
                        name, log.id, ctx.obj.project_id
                    )
                    print()
                    print(log_with_value.value)
            else:
                print(
                    tabulate(
                        [x.dict().values() for x in logs],
                        headers=Log.get_field_names(),
                        tablefmt="psql",
                    )
                )
    except TimonApiException as e:
        logger.error(str(e))


@app.command("states")
def get_deployment_states(
    ctx: typer.Context, name: str, version_id: str = typer.Argument(default=None)
):
    try:
        if not version_id:
            states = ctx.obj.client.get_deployment_states(name, ctx.obj.project_id)
            print(
                tabulate(
                    [x.values() for x in states],
                    headers=["version_id", "last_modified"],
                    tablefmt="psql",
                )
            )
        else:
            state = ctx.obj.client.get_deployment_state(
                name, version_id, ctx.obj.project_id
            )
            with open(f"{version_id}.tar", "wb") as fp:
                fp.write(state)
            print(f"State downloaded and saved to {version_id}.tar")

    except TimonApiException as e:
        logger.error(str(e))


@app.command()
def control(ctx: typer.Context, name: str):
    try:
        deployment = ctx.obj.client.get_deployment(name, ctx.obj.project_id)

        if deployment.status in [DeploymentStatus.reconciled, DeploymentStatus.created]:
            template = ctx.obj.client.get_template(
                deployment.template_id, ctx.obj.project_id
            )
            blueprint = ctx.obj.client.get_blueprint(
                template.blueprint_id, ctx.obj.project_id
            )

            if not blueprint.control:
                logger.error(f"Console not supported by deployment {name}")

            else:
                data_outputs = ctx.obj.client.get_deployment_outputs(
                    name, None, ctx.obj.project_id
                )
                template_data = {
                    "outputs": SimpleNamespace(**data_outputs),
                }
                control = json.loads(blueprint.control)
                parsed_arguments = {}
                for argument in control["arguments"]:
                    template = jinja2.Environment(loader=jinja2.BaseLoader).from_string(
                        argument["value"]
                    )
                    parsed_arguments[argument["name"]] = template.render(
                        **template_data
                    )

                if control["type"] == "ssh":
                    with tempfile.NamedTemporaryFile() as t:
                        os.chmod(t.name, 0o600)
                        with open(t.name, "w+") as fp:
                            fp.write(parsed_arguments["identity_file"])

                        ssh_arguments = "-o LogLevel=ERROR -o StrictHostKeyChecking=no"
                        command = f"ssh {ssh_arguments} -i {fp.name} {parsed_arguments['user']}@{parsed_arguments['destination']}"
                        subprocess.call(command, shell=True)
                else:
                    logger.error(f"Console type {control['type']} not supported")
        else:
            logger.error(
                f"Deployment is in state {deployment.status}, it has to be in state RECONCILED or CREATED"
            )

    except TimonApiException as e:
        logger.error(str(e))
