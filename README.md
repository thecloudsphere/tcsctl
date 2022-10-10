# Welcome to Timon

Timon efficiently manages your cloud infrastructures 🚀

Automate infrastructure as code (IaC) provisioning at any scale,
at any cloud or data center with any tool. Through a single central
API. Freely definable cloud infrastructures at the push of a button
as self-service.

## Getting started

Install the CLI for Timon with ``pip3 install timonctl``.

Prerequisite for the use is an account on our public service or on a
local on-premise installation.

Create the file ``timon.yaml`` which contains the details of the API and
the authentication details.

```
# log_level: DEBUG
profiles:
  default:
    api_url: https://timon.osism.tech/api/
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
timonctl validate config timon.yaml
Config timon.yaml is valid.
```

Before you can use the CLI, you have to log in.

```
timonctl login
Password:
Logged in successfully.
```

Create the file ``sample.yaml`` which contains a sample template for a
deployment with Terraform on an OpenStack environment.

```
terraform-sample:
  environment:
    name: terraform/openstack
    repository: timontech/registry
    repository_server: https://github.com
  blueprint:
    name: terraform/openstack/minimal
    repository: timontech/registry
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
timonctl validate template sample.yaml
Template sample.yaml is valid.
```

This example uses a ``clouds.yaml`` file, which is located in the same directory
as the ``sample.yaml`` file. The content of this file depends very much on the
OpenStack environment used. Refer to the documentation of the operator of the
OpenStack environment accordingly.

Import the template ``terraform-sample`` defined in the previously created
``sample.yaml`` file.

```
timonctl template import sample.yaml terraform-sample
```

A deployment ``hello-world`` can now be created from the template
``terraform-sample``.

```
timonctl deployment create hello-world terraform-sample
```

Once the deployment has been created, the public IP address and the SSH keypair
for the login can be retrieved via the outputs.

```
timonctl deployment outputs hello-world address
10.100.3.41
```

```
timonctl deployment outputs hello-world private_key
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA1aiAph+QxP0dp18b04b24oE8+e4FFdxULeKiT4vZssuVRrFy
[...]
```

The logs that were printed during the creation of the deployment can
be displayed using the timonctl deployments logs command.

```
timonctl deployment logs --show hello-world create
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
timonctl deployment destroy hello-world
```

All logs from a specific period for a deployment can also be displayed.

```
timonctl deployment logs hello-world '15 minutes ago'
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
timonctl deployment logs hello-world b0765dac-2f1b-4d7b-84fc-85e328bfa018
openstack_compute_keypair_v2.timon: Refreshing state... [id=terraform-keypair]
data.openstack_networking_network_v2.public: Reading...
openstack_networking_network_v2.timon: Refreshing state... [id=23b0a0e1-e560-4b50-9bd8-4b7ca9cfc203]
openstack_compute_secgroup_v2.timon: Refreshing state... [id=3db448c1-9a3c-495b-aec8-514fd774fdf8]
local_sensitive_file.private_key: Refreshing state... [id=14070ff949339f2a7eb97690cd4f3f7a0c13e2a3]
openstack_networking_subnet_v2.timon: Refreshing state... [id=acfb2765-e522-41c1-9178-fab084611a1c]
[...]
```

After a deployment has been destroyed, it can be deleted. All associated logs
are then also deleted.

```
timonctl deployment delete hello-world
```

If you no longer need to use the CLI, you can log out.

```
timonctl logout
Logged out successfully.
```
