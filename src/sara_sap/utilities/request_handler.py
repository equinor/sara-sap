import warnings
from typing import Any, Optional

import requests
from loguru import logger
from requests.exceptions import HTTPError, RequestException
from requests.models import Response

from sara_sap.settings import settings


def _base_request(
    url: str,
    method: str,
    headers: Optional[dict],
    json_body: Any,
    timeout: Optional[float],
    data: Any = None,
    params: Optional[dict] = None,
    **kwargs,
) -> Response:
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            response = requests.request(
                url=url,
                method=method,
                headers=headers,
                timeout=timeout,
                json=json_body,
                data=data,
                params=params,
                verify=False,
                **kwargs,
            )
    except RequestException as e:
        raise e
    except Exception as e:
        logger.exception("An unhandled exception occurred during a request")
        raise RequestException from e

    try:
        response.raise_for_status()
    except HTTPError as e:
        response_dict: dict = e.response.json()

        try:
            error_message = response_dict["detail"]
            raise RequestException(error_message)
        except KeyError:
            logger.exception(
                f"Http error. Http status code= {response.status_code}. Http response body= {response.json()}"
            )
            raise RequestException from e
    return response


def get(
    url: str,
    json_body=None,
    request_timeout: Optional[float] = settings.API_REQUEST_TIMEOUT,
    headers: Optional[dict] = None,
    data: Optional[dict] = None,
    stream: bool = False,
    params: Optional[dict] = None,
    **kwargs,
) -> Response:
    return _base_request(
        url=url,
        method="GET",
        headers=headers,
        timeout=request_timeout,
        json_body=json_body,
        data=data,
        stream=stream,
        params=params,
        **kwargs,
    )


def post(
    url: str,
    json_body=None,
    request_timeout: Optional[float] = settings.API_REQUEST_TIMEOUT,
    headers: Optional[dict] = None,
    data: Any = None,
    params: Optional[dict] = None,
    **kwargs,
) -> Response:
    return _base_request(
        url=url,
        method="POST",
        headers=headers,
        timeout=request_timeout,
        json_body=json_body,
        data=data,
        params=params,
        **kwargs,
    )


def patch(
    url: str,
    json_body=None,
    request_timeout: Optional[float] = settings.API_REQUEST_TIMEOUT,
    headers: Optional[dict] = None,
    data: Any = None,
    params: Optional[dict] = None,
    **kwargs,
) -> Response:
    return _base_request(
        url=url,
        method="PATCH",
        headers=headers,
        timeout=request_timeout,
        json_body=json_body,
        data=data,
        params=params,
        **kwargs,
    )
