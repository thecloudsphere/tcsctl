from enum import unique, Enum


@unique
class DeploymentAction(str, Enum):
    create = "CREATE"
    destroy = "DESTROY"
    none = "NONE"
    reconcile = "RECONCILE"


@unique
class DeploymentType(str, Enum):
    flow = "FLOW"
    environment = "ENVIRONMENT"


@unique
class DeploymentStatus(str, Enum):
    check = "CHECK"
    create = "CREATE"
    created = "CREATED"
    destroy = "DESTROY"
    destroyed = "DESTROYED"
    error = "ERROR"
    initialize = "INITIALIZE"
    none = "NONE"
    reconcile = "RECONCILE"
    reconciled = "RECONCILED"
    validate = "VALIDATE"


@unique
class FlowAction(str, Enum):
    create = "CREATE"
    destroy = "DESTROY"
    none = "NONE"


@unique
class FlowStatus(str, Enum):
    create = "CREATE"
    created = "CREATED"
    destroy = "DESTROY"
    destroyed = "DESTROYED"
    none = "NONE"


@unique
class Visibility(str, Enum):
    community = "COMMUNITY"
    private = "PRIVATE"
    public = "PUBLIC"
    shared = "SHARED"
