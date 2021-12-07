from app.models.errors import Error


def test_error_model():
    _error: Error = Error(
        **{
            "error_code": "FAKE_ERROR_CODE",
            "error_message": "FAKE_ERROR_MESSAGE",
        }
    )
    assert _error.error_code == "FAKE_ERROR_CODE"
    assert _error.error_message == "FAKE_ERROR_MESSAGE"
    assert _error.error_deails == ""
