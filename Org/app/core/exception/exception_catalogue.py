from app.models.errors import Error


class ExceptionCatalogue:
    DEFAULT_ERROR = Error(error_code="WARG_999", error_message="")
    MONGO_DB_ERROR = Error(
        error_code="WARG_001", error_message="MONGODB Error"
    )
    NO_RESOURCE_ERROR = Error(
        error_code="WARG_002", error_message="NO resource found"
    )
