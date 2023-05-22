"""
ICS API Exceptions module
"""

from requests.exceptions import HTTPError, RequestException, JSONDecodeError

class HTTPNotFound(HTTPError):
    """Api Key not found"""

class HTTPBadRequest(HTTPError):
    """Invalid API request"""

class HTTPForbidden(HTTPError):
    """Access forbidden"""

class HTTPUnprocessableEntity(HTTPError):
    """Entity cannot be created"""

class InvalidContent(HTTPError):
    """Invalid content type received"""
