from datetime import datetime
from decimal import Decimal
from uuid import UUID

from fastapi import status
from fastapi.responses import JSONResponse
from typing import Any, Union, List


def success_response_with_data(
    message: str = "Operation successful.",
    data: Any = None,
    status_code=status.HTTP_200_OK,
) -> JSONResponse:
    return JSONResponse(
        content={"message": message, "data": data, "error": False},
        status_code=status_code,
    )


def success_response(
    message: str = "Operation successful.",
    status_code=status.HTTP_200_OK,
) -> JSONResponse:
    return JSONResponse(
        content={"message": message, "error": False},
        status_code=status_code,
    )


def error_response(
    message: str,
    details: Union[None, str, list] = None,
    status_code=status.HTTP_400_BAD_REQUEST,
) -> JSONResponse:
    if isinstance(details, str):
        details = [details]
    return JSONResponse(
        content={"message": message, "details": details, "error": True},
        status_code=status_code,
    )


def jwt_response_error(
    message: str,
    details: Union[None, str, list] = None,
    status_code=status.HTTP_401_UNAUTHORIZED,
) -> JSONResponse:
    return JSONResponse(
        content={"message": message, "details": details, "error": True},
        status_code=status_code,
    )


def serialize_data(data: Any) -> Any:
    if isinstance(data, list):
        return [serialize_data(item) for item in data]
    elif isinstance(data, dict):
        return {key: serialize_data(value) for key, value in data.items()}
    elif isinstance(data, datetime):
        return data.isoformat()
    elif isinstance(data, UUID):
        return str(data)
    elif isinstance(data, Decimal):
        return float(data)
    return data


def list_response(
    data,
    count: int,
    limit: int,
    offset: int,
    base_url: str,
    message: str = "Operation successful.",
    status_code=status.HTTP_200_OK,
) -> JSONResponse:
    current = (offset // limit) + 1
    next_url = None
    previous_url = None

    if offset + limit < count:
        next_url = f"{base_url}?limit={limit}&offset={offset + limit}"

    if offset > 0:
        previous_url = f"{base_url}?limit={limit}&offset={max(offset - limit, 0)}"

    response_content = {
        "message": message,
        "data": {
            "count": count,
            "current": current,
            "next": next_url,
            "previous": previous_url,
            "limit": limit,
            "results": data,
        },
        "error": False,
    }

    return JSONResponse(
        content=response_content,
        status_code=status_code,
    )


def paginated_list_response(
    data,
    count: int,
    limit: int,
    offset: int,
    base_url: str,
    status_code=status.HTTP_200_OK,
) -> JSONResponse:
    current = (offset // limit) + 1
    next_url = None
    previous_url = None

    if offset + limit < count:
        next_url = f"{base_url}?limit={limit}&offset={offset + limit}"

    if offset > 0:
        previous_url = f"{base_url}?limit={limit}&offset={max(offset - limit, 0)}"

    response_content = {
        "count": count,
        "current": current,
        "next": next_url,
        "previous": previous_url,
        "limit": limit,
        "results": data,
    }

    return JSONResponse(
        content=response_content,
        status_code=status_code,
    )


def permission_error_response(
    message: str,
    details: Union[None, str, list] = None,
    status_code=status.HTTP_403_FORBIDDEN,
) -> JSONResponse:
    return JSONResponse(
        content={"message": message, "details": details, "error": True},
        status_code=status_code,
    )
