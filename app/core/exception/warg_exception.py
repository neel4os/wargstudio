from app.models.errors import Error


class WargException(Exception):
    def __init__(self, status_code: int, error: Error, error_details : str) -> None:
        self._model = error
        self._status_code = status_code
        self._model.error_details = error_details
