from typing import Any, Dict
from requests import Response
from django.conf import settings
from vanoma_api_utils.http import client
from djangorestframework_camel_case.util import camelize  # type: ignore


class AuthApiException(Exception):
    pass


def create_login(data: Dict[str, Any]) -> Response:
    response = client.post(
        f"{settings.VANOMA_AUTH_API_URL}/login-creation",
        data=camelize(data),
    )

    if not response.ok:
        json = response.json()
        raise AuthApiException(json["errorMessage"])

    return response


def sign_in(data: Dict[str, Any]) -> Response:
    response = client.post(
        f"{settings.VANOMA_AUTH_API_URL}/sign-in",
        data=camelize(data),
    )

    if not response.ok:
        json = response.json()
        raise AuthApiException(json["errorMessage"])

    return response
