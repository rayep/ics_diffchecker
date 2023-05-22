"""ICS Diffchecker - VLAN source IP"""

import getpass
from ics_diffchecker.rest.client import APIClient
from ics_diffchecker.rest.auth import APIKeyGenerator
from ics_diffchecker.models.role import UserRoleModel
from ics_diffchecker.services.role import UserRoleService, UserRoleCompare


def get_hostname(device_type:str):
    """Parse hostname"""
    host = input(f'{device_type} VPN Hostname/IP: ')
    hostname = host.replace(
        'https://', '') if host.startswith('https://') else host
    return hostname

def get_api_key(hostname: str) -> str:
    """Get REST API key"""
    username = input('Admin username: ')
    password = getpass.getpass(prompt='Admin password: ', stream=None)
    key_request = APIKeyGenerator(
        host=hostname, username=username, password=password)
    return key_request.api_key


# Source section
print()
src_hostname = get_hostname("Source")
src_key = get_api_key(src_hostname)
client = APIClient(src_hostname, src_key)

src_roles = UserRoleService(client, src_hostname)
selected_src_roles = src_roles.fetch(roles=src_roles.roles)

src_role_models = UserRoleModel(selected_src_roles)
src_user_roles = src_role_models.create()


# Target section
print()
trgt_hostname = get_hostname("Target")
trgt_key = get_api_key(trgt_hostname)
client = APIClient(trgt_hostname, trgt_key)

tgrt_roles = UserRoleService(client, trgt_hostname)
selected_trgt_roles = src_roles.fetch(roles=tgrt_roles.roles)

trgt_role_models = UserRoleModel(selected_trgt_roles)
trgt_user_roles = trgt_role_models.create()


# VLAN source IP compare

compare = UserRoleCompare(src_user_roles, trgt_user_roles)
compare.vlan_check()
print("*** Done ***")
