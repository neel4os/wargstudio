from app.models.errors import Error


class ExceptionCatalogue:
    DEFAULT_ERROR = Error(error_code="WARG_999", error_message="")
    MONGO_DB_ERROR = Error(
        error_code="WARG_001", error_message="MONGODB Error"
    )
    NO_RESOURCE_ERROR = Error(
        error_code="WARG_002", error_message="No resource found"
    )
    VALIDATION_ERROR = Error(
        error_code="WARG_003",
        error_message="Validation Failed for payload",
    )
    STORAGE_ERROR = Error(
        error_code="WARG_004",
        error_message="An error encountered in Storage",
    )

