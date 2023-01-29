# Welcome to The Cloudsphere

The Cloudsphere efficiently manages your cloud infrastructures 🚀

Automate infrastructure as code (IaC) provisioning at any scale,
at any cloud or data center with any tool. Through a single central
API. Freely definable cloud infrastructures at the push of a button
as self-service.

## Getting started

Install the CLI for The Cloudsphere with ``pip3 install tcsctl``.

Prerequisite for the use is an account on our public service or on a
local on-premise installation.

Create the file ``tcs.yaml`` which contains the details of the API and
the authentication details.

```
# log_level: DEBUG
profiles:
  default:
    api_url: https://api.demo.thecloudsphere.io/api/
    api_version: v1
    insecure: false
    auth:
      organisation: Sample
      project: Sample
      username: sample
      # password: password
```

To be sure, check that the configuration is valid.

```
tcsctl validate config tcs.yaml
Config tcs.yaml is valid.
```

Before you can use the CLI, you have to log in.

```
tcsctl login
Password:
Logged in successfully.
```

Create the file ``sample.yaml`` which contains a sample template for a
deployment with Terraform on an OpenStack environment.

```
terraform-sample:
  environment:
    name: terraform/openstack
    repository: thecloudsphere/registry
    repository_server: https://github.com
  blueprint:
    name: terraform/openstack/minimal
    repository: thecloudsphere/registry
    repository_server: https://github.com
  blueprint_version: main
  inputs:
    prefix: terraform
    clouds.yaml:
      type: file
      path: clouds.yaml
    "cloud name": openstack
    flavor: "SCS-1V:1:10"
    "public network": public
```

To be sure, check that the template is valid.

```
tcsctl validate template sample.yaml
Template sample.yaml is valid.
```

This example uses a ``clouds.yaml`` file, which is located in the same directory
as the ``sample.yaml`` file. The content of this file depends very much on the
OpenStack environment used. Refer to the documentation of the operator of the
OpenStack environment accordingly.

Import the template ``terraform-sample`` defined in the previously created
``sample.yaml`` file.

```
tcsctl template import sample.yaml terraform-sample
+---------------------+--------------------------------------+
| Field               | Value                                |
|---------------------+--------------------------------------|
| blueprint_id        | 803f3163-66b7-4c21-9c42-ef92fdb96fa6 |
| blueprint_version   | main                                 |
| environment_id      | d4135a7b-4eff-4e25-9f61-618b81b9a147 |
| environment_version |                                      |
| name                | terraform-sample                     |
| id                  | 05aa4b88-50ed-4dd1-8006-64772ae3f0f9 |
| created_at          | 2023-01-28 22:26:02                  |
+---------------------+--------------------------------------+
```

Blueprints and environments can be listed to verify the import.

```
tcsctl environment list
+---------------------+--------------------+-------------------+---------------------+--------------------------------------+---------------------+
| name                | repository         | repository_path   | repository_server   | id                                   | created_at          |
|---------------------+--------------------+-------------------+---------------------+--------------------------------------+---------------------|
| terraform/openstack | thecloudsphere/registry | environments      | https://github.com  | d4135a7b-4eff-4e25-9f61-618b81b9a147 | 2023-01-28 22:26:01 |
+---------------------+--------------------+-------------------+---------------------+--------------------------------------+---------------------+

tcsctl blueprint list
+-----------------------------+--------------------+-------------------+---------------------+--------------------------------------+---------------------+
| name                        | repository         | repository_path   | repository_server   | id                                   | created_at          |
|-----------------------------+--------------------+-------------------+---------------------+--------------------------------------+---------------------|
| terraform/openstack/minimal | thecloudsphere/registry | blueprints        | https://github.com  | 803f3163-66b7-4c21-9c42-ef92fdb96fa6 | 2023-01-28 22:26:02 |
+-----------------------------+--------------------+-------------------+---------------------+--------------------------------------+---------------------+
```

A deployment ``hello-world`` can now be created from the template
``terraform-sample``.

```
tcsctl deployment create hello-world terraform-sample
+-----------------+--------------------------------------+
| Field           | Value                                |
|-----------------+--------------------------------------|
| name            | hello-world                          |
| template_id     | 05aa4b88-50ed-4dd1-8006-64772ae3f0f9 |
| id              | 5fe18e39-1b5a-4d0e-8760-448b6cf2ab19 |
| created_at      | 2023-01-28 22:35:54                  |
| action          | CREATE                               |
| deployment_type | ENVIRONMENT                          |
| status          | NONE                                 |
+-----------------+--------------------------------------+
```

When the orchestrator selects the deployment for execution, the status is changed
from ``NONE`` to ``CREATE``.

```
tcsctl deployment list --column name --column status
+----+-------------+----------+
|    | name        | status   |
|----+-------------+----------|
|  0 | hello-world | CREATE   |
+----+-------------+----------+
```

Once the deployment has been created the status changes to ``CREATED``.

```
tcsctl deployment list --column name --column status
+----+-------------+----------+
|    | name        | status   |
|----+-------------+----------|
|  0 | hello-world | CREATED  |
+----+-------------+----------+
```

The public IP address and the SSH keypair for the login can then be retrieved via
the ``outputs`` command.

```
tcsctl deployment outputs hello-world address
10.100.3.41
```

```
tcsctl deployment outputs hello-world private_key
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA1aiAph+QxP0dp18b04b24oE8+e4FFdxULeKiT4vZssuVRrFy
[...]
```

With ``tcsctl deployment outputs hello-world`` it is possible to output all
available outputs.

With the parameter ``--file``, the output can be written directly to a file.

```
tcsctl deployment outputs hello-world private_key --file id_rsa.hello-world
Output private_key from deployment hello-world was written to file id_rsa.hello-world.
```

The logs that were printed during the creation of the deployment can
be displayed using the ``tcsctl deployments logs`` command.

```
tcsctl deployment logs --show hello-world create
data.openstack_networking_network_v2.public: Reading...
data.openstack_networking_network_v2.public: Read complete after 1s [id=665eea18-2b85-427c-b0bf-a6fd040cc0fc]

Terraform used the selected providers to generate the following execution
plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # local_sensitive_file.address will be created
[...]
```

If the deployment is no longer needed, it can be destroyed.

```
tcsctl deployment destroy hello-world
```

All logs from a specific period for a deployment can also be displayed.

```
tcsctl deployment logs hello-world '15 minutes ago'
+------------+--------------------------------------+---------------------+
| category   | id                                   | created_at          |
|------------+--------------------------------------+---------------------|
| import     | af7cd606-5e7b-4d34-9bd7-89d43efc2f29 | 2022-10-09 17:30:01 |
| export     | 3d10733e-670f-45b0-865c-851171982670 | 2022-10-09 17:30:04 |
| reconcile  | 7cd79e0f-a56e-436a-be08-cdf0529febe5 | 2022-10-09 17:30:04 |
| import     | 1b2d5c04-2860-45f2-a6ce-bdd6b851d896 | 2022-10-09 17:31:20 |
| destroy    | b0765dac-2f1b-4d7b-84fc-85e328bfa018 | 2022-10-09 17:31:51 |
| export     | f774401e-5b23-4c86-bc10-34ca840f155c | 2022-10-09 17:31:51 |
+------------+--------------------------------------+---------------------+
```

The ID of a log entry can be used to display a specific log entry.

```
tcsctl deployment logs hello-world b0765dac-2f1b-4d7b-84fc-85e328bfa018
openstack_compute_keypair_v2.tcs: Refreshing state... [id=terraform-keypair]
data.openstack_networking_network_v2.public: Reading...
openstack_networking_network_v2.tcs: Refreshing state... [id=23b0a0e1-e560-4b50-9bd8-4b7ca9cfc203]
openstack_compute_secgroup_v2.tcs: Refreshing state... [id=3db448c1-9a3c-495b-aec8-514fd774fdf8]
local_sensitive_file.private_key: Refreshing state... [id=14070ff949339f2a7eb97690cd4f3f7a0c13e2a3]
openstack_networking_subnet_v2.tcs: Refreshing state... [id=acfb2765-e522-41c1-9178-fab084611a1c]
[...]
```

After a deployment has been destroyed, it can be deleted. All associated logs
are then also deleted.

```
tcsctl deployment delete hello-world
```

If you no longer need to use the CLI, you can log out.

```
tcsctl logout
Logged out successfully.
```
