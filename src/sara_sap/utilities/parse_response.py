from typing import TypeVar, Type

from fastapi import HTTPException
from loguru import logger
from pydantic import ValidationError, TypeAdapter
from requests import Response, JSONDecodeError

TModel = TypeVar("TModel", bound=object)


def parse_response_into_model(response: Response, model_type: Type[TModel]) -> TModel:
    try:
        payload: dict = response.json()
    except JSONDecodeError as e:
        error_description: str = (
            f"Failed to decode JSON response when requesting model type {model_type.__name__} through Maintenance API. "
            f"The response content was: {response.content}"
        )
        logger.exception(error_description)
        raise HTTPException(status_code=500, detail=error_description) from e

    try:
        return TypeAdapter(model_type).validate_python(payload)
    except ValidationError as e:
        error_description: str = (
            f"A validation error occurred when parsing into object of type {model_type.__name__} "
            f"from Maintenance API. The JSON attempted parsed was: {response.json()}"
        )
        logger.exception(error_description)
        raise HTTPException(status_code=500, detail=error_description) from e
