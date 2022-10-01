from enum import unique, Enum


@unique
class DeploymentAction(str, Enum):
    create = "CREATE"
    destroy = "DESTROY"
    none = "NONE"
    reconcile = "RECONCILE"


@unique
class Visibility(str, Enum):
    community = "COMMUNITY"
    private = "PRIVATE"
    public = "PUBLIC"
    shared = "SHARED"
