"""Utils for ICS REST Sessions."""

from json import dumps
from requests import Response
from .misc import HOST
from .exceptions import (
    HTTPError,
    HTTPUnprocessableEntity,
    HTTPForbidden,
    HTTPBadRequest,
    HTTPNotFound,
    InvalidContent,
    JSONDecodeError
    )

def raise_exception(data: Response, exception: str) -> None:
    """Raises exception based on the HTTP status code"""
    message = parse_error_message(data)
    if data.status_code == 422:
        raise HTTPUnprocessableEntity(message) from None
    if data.status_code == 400:
        raise HTTPBadRequest(message) from None
    if data.status_code == 403:
        raise HTTPForbidden(exception) from None
    if data.status_code == 404:
        raise HTTPNotFound(message) from None

def hook_raise_status(data: Response, *args, **kwargs):
    """Check for return status code"""
    try:
        data.raise_for_status()
    except HTTPError as exception:
        raise_exception(data, exception)
    return data

def hook_api_key(data: Response, *args, **kwargs) -> str:
    """Hook function to return the API Key value as api_key attribute of response obj"""
    if not data.headers['Content-Type'] == "application/json":
        raise InvalidContent(f"Invalid Content type received: {data.headers.get('Content-Type')}")
    data.api_key = data.json()['api_key']
    return data

def hook_get_response(data: Response, *args, **kwargs):
    """Pretty print for JSON response"""
    data.pretty = dumps(data.json(), indent=1)
    return data

def hook_put_post_delete_response(data: Response, *args, **kwargs):
    """Pretty print for JSON response"""
    if int(data.headers['Content-Length']) > 0:
        # DELETE returns no content length.
        data.pretty = dumps(data.json(), indent=1)
        # Adding "pretty" attr regardless of the response type.
        # if data.status_code in range(200, 299):
        try:
            result_warn = data.json()['result']['warnings']
            data.message = result_warn[-1]['message']
            return data
        except KeyError:
            # try parsing info section out from the message.
            try:
                result_warn = data.json()['result']['info']
                data.message = result_warn[-1]['message']
                return data
            except KeyError:
                data.message = None
    data.message = None
    return data

def get_host_value(data) -> dict:
    """Returns the data"""
    HOST.setdefault('host', data)
    return HOST

def parse_error_message(data: Response) -> str:
    """Get the error message from 4XX/5XX responses"""
    try:
        result_error = data.json()['result']['errors']
        message = result_error[-1]['message']
        return message
    except (JSONDecodeError, KeyError):
        return ''
