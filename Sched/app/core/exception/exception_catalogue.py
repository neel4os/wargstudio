from app.models.errors import Error


class ExceptionCatalogue:
    DEFAULT_ERROR = Error(error_code="SCHED_999", error_message="")
    NO_RESOURCE_ERROR = Error(
        error_code="SCHED_002", error_message="No resource found"
    )
    VALIDATION_ERROR = Error(
        error_code="SCHED_003",
        error_message="Validation Failed for payload",
    )
    STORAGE_ERROR = Error(
        error_code="SCHED_004",
        error_message="An error encountered in Storage",
    )

