import enum


class DeploymentAction(enum.Enum):
    create = "create"
    destroy = "destroy"
    reconcile = "reconcile"


class Visibility(enum.Enum):
    community = "COMMUNITY"
    private = "PRIVATE"
    public = "PUBLIC"
    shared = "SHARED"
