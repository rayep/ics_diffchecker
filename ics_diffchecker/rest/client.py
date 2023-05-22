"""Main Requests module for REST API calls"""

from posixpath import join as urljoin
from urllib3 import disable_warnings
import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import ConnectionError as ConnectError, Timeout
from .utils import (
    hook_get_response,
    hook_raise_status,
    get_host_value,
    hook_put_post_delete_response
    )
from .misc import DEFAULT_HEADERS, HOST
disable_warnings()  # Function to suppress the SSL Verification error.


def exception_handler(func):
    """Generic Exception handler for APIClient requests

    :hooks
    hook_raise_status calls response.raise_for_status()
    hook_pretty_print for adding "ppjson" attribute to Response object.
    """
    def wrapper(*args, **kwargs):
        try:
            if func.__name__ == 'get':
                kwargs.update(
                {'hooks': {'response': [hook_raise_status, hook_get_response]}})
            else:
                kwargs.update(
                {'hooks': {'response': [hook_raise_status, hook_put_post_delete_response]}})
            kwargs.update({'timeout': 20})
            kwargs.update(
                {'url': kwargs.get('url')
                    if 'https' in kwargs.get('url')
                    else urljoin('https://'+HOST.get('host')+kwargs.get('url'))})
            response = func(*args, **kwargs)
            return response
        except (ConnectError, Timeout) as exc:
            raise SystemExit(f"Requests Exception: {exc}") from None
    return wrapper


class APIClient:
    """REST API Client compatible with PCS/ICS servers
    
    @params:
    - host: VPN server hostname or IP
    - api_key: API Key"""

    def __init__(self, host: str, api_key: str, **kwargs):

        self.api_key = HTTPBasicAuth(api_key, '')
        self.headers = DEFAULT_HEADERS if kwargs.get('headers') is None \
            else DEFAULT_HEADERS | kwargs.get('headers')
        get_host_value(host)  # Updating the HOST constant.
        self.session = requests.session()
        self.session.auth = self.api_key or {}
        self.session.headers = self.headers or {}
        self.session.proxies = kwargs.get('proxy') or {}
        self.session.verify = False

    @exception_handler
    def get(self, **kwargs):
        """GET Request"""
        return self.session.get(**kwargs)

    @exception_handler
    def post(self, data=None, **kwargs):
        """POST Request"""
        return self.session.post(json=data, **kwargs)

    @exception_handler
    def put(self, data=None, **kwargs):
        """PUT Request"""
        return self.session.put(json=data, **kwargs)

    @exception_handler
    def delete(self, **kwargs):
        """DELETE Request"""
        return self.session.delete(**kwargs)
