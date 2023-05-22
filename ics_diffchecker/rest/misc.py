"""Misc tools that powers the api_requests module."""

from platform import python_version,system,machine

__version__ = 1.0

def user_agent():
    """Creates UA based on the system type"""
    py_version = python_version()
    os_build = system()
    os_arch = machine()
    return f"Ray's API Client/{__version__} (python {py_version}; os {os_build}; arch {os_arch})"

DEFAULT_HEADERS = {
    'User-Agent': f"{user_agent()}",
    'Accept': "*/*"
}

HOST = {}
