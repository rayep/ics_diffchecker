"""
ICS API Key Generator
"""
from posixpath import join as urljoin
from requests import get, Response
from requests.auth import HTTPBasicAuth
from urllib3 import disable_warnings
from .misc import DEFAULT_HEADERS
from .utils import hook_raise_status, hook_api_key
from .exceptions import RequestException, HTTPForbidden, HTTPError

disable_warnings()  # Function to suppress the SSL Verification error.


class APIKeyGenerator:
    """PCS/ICS REST API Key Generator"""

    def get_api_key(self) -> Response:
        """API Key auth"""

        try:
            response: Response = get(
                url=urljoin(self.host, 'api/v1/auth'),
                headers=DEFAULT_HEADERS,
                verify=False,
                allow_redirects=False,
                timeout=30,
                auth=HTTPBasicAuth(self.username, self.password),
                hooks={'response': [hook_raise_status, hook_api_key]}
            )
            self.api_key = response.api_key
        except HTTPForbidden:
            raise SystemExit(
                "*** API authentication failed. Please check your credentials! ***") from None
        except (RequestException, HTTPError) as exc:
            raise SystemExit(exc) from None
        except AttributeError:
            raise SystemExit(
                "*** API Key not found. Please check your VPN server URL ***") from None
        return response

    def __str__(self) -> str:
        """Prints API Key"""
        return self.api_key

    def __init__(
            self,
            host: str,
            username: str,
            password: str) -> None:
        """PCS/ICS REST API Key Generator"""

        self.host: str = host if host.startswith(
            'https') else urljoin('https://', host)
        self.username: str = username
        self.password: str = password
        self.api_key = ''
        self.get_api_key()
