# timonctl

| :memo: | Timon is a work in progress. Features will evolve over time and there may be breaking changes between releases. |
|-|:-|

## Usage

### common

```
❯ timonctl --help

 Usage: timonctl [OPTIONS] COMMAND [ARGS]...

╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────╮
│ --profile                   TEXT  [env var: TIMON_PROFILE] [default: default]                       │
│ --install-completion              Install completion for the current shell.                         │
│ --show-completion                 Show completion for the current shell, to copy it or customize    │
│                                   the installation.                                                 │
│ --help                            Show this message and exit.                                       │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ──────────────────────────────────────────────────────────────────────────────────────────╮
│ blueprint                                                                                           │
│ environment                                                                                         │
│ login                                                                                               │
│ logout                                                                                              │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

### blueprints

List all blueprints assigned to a specific project:

```
❯ timonctl blueprint list 3ad7cbf4-5e50-41d3-86f8-b8d95efeec7f
+--------------------------------------+---------------------+---------------------+-----------------------------+
| id                                   | created_at          | updated_at          | name                        |
|--------------------------------------+---------------------+---------------------+-----------------------------|
| fb6ac1a2-4870-4eb3-b5af-624b2d967dd3 | 2022-09-28 19:59:34 | 2022-09-28 20:00:49 | terraform/openstack/minimal |
+--------------------------------------+---------------------+---------------------+-----------------------------+
```

### environments

List all environments assigned to a specific project:

```
❯ timonctl environment list 3ad7cbf4-5e50-41d3-86f8-b8d95efeec7f
+--------------------------------------+---------------------+---------------------+----------------+
| id                                   | created_at          | updated_at          | name           |
|--------------------------------------+---------------------+---------------------+----------------|
| 42e8579f-5f75-444e-a73d-874e150fa88b | 2022-09-28 19:26:10 | 2022-09-28 19:27:32 | terraform/base |
+--------------------------------------+---------------------+---------------------+----------------+
```

## Configuration

```
---
profiles:
  default:
    api_url: http://api.timon.osism.tech/api/
    api_version: 1
    auth:
      username:
      organisation_name:
      project_name:
      password:
      # token_id:
      # token_secret:
```
