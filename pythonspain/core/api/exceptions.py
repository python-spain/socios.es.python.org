from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError as DRFValidationError


def extra_exception_handler(exc, context):
    # from https://gist.github.com/twidi/9d55486c36b6a51bdcb05ce3a763e79f
    # Convert django ValidationError to DRF exceptions. This way, instead of
    # returning a 500 error it will return a 400
    if isinstance(exc, DjangoValidationError):
        errors = getattr(exc, "error_list", None) or getattr(exc, "error_dict", None)
        exc = DRFValidationError(detail=errors)

    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # If response is None, add more cases to the exception handler.
    if response is None:
        if isinstance(exc, IntegrityError):
            data = {api_settings.NON_FIELD_ERRORS_KEY: str(exc)}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        elif (
            isinstance(exc, APIException)
            and exc.status_code == status.HTTP_400_BAD_REQUEST
        ):
            data = {
                api_settings.NON_FIELD_ERRORS_KEY: exc.get_full_details()["message"],
                "code": exc.get_codes(),
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    # If the response has APIException inject the exception code in the response
    elif response and isinstance(exc, APIException) and exc.get_codes():
        response.data["code"] = exc.get_codes()

    return response
