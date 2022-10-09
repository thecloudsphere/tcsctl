# Welcome to Timon

Timon efficiently manages your cloud infrastructures 🚀

Automate infrastructure as code (IaC) provisioning at any scale,
at any cloud or data center with any tool. Through a single central
API. Freely definable cloud infrastructures at the push of a button
as self-service.

## Getting started

Install the CLI for Timon with ``pip3 install timonctl``.

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

Import the template ``terraform-sample`` defined in the previously created
``sample.yaml`` file.

```
timonctl template import sample.yaml terraform-sample
```

A deployment ``hello-world`` can now be created from the template
``terraform-sample``.

```
timonctl deployment create hello-world terraform-sample
