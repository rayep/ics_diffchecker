"""Service - Roles"""

import time


class UserRoleService():
    """Get all User roles from ICS
    Low level service that fetches the available user roles from ICS servers using enum_roles & get_roles URL"""

    enum_roles = '/api/v1/configuration/users/user-roles'
    get_role = '/api/v1/configuration/users/user-roles/user-role/'

    def __init__(self, rest_client, hostname: str) -> None:
        self.client = rest_client
        self.hostname = hostname
        self.roles = []
        self._enumerate()

    def _enumerate(self):
        roles = self.client.get(url=self.enum_roles)
        self.roles.extend(sorted([role['name']
                          for role in roles.json()['user-role']]))

    def fetch(self, roles: list):
        """Parse user roles from API response.
        parsed_roles list contains dict of all user roles JSON content"""
        parsed_roles = []
        roles = roles if roles else self.roles
        for role in roles:
            print(f"Fetching user role '{role}' data")
            response = self.client.get(url=self.get_role+role)
            parsed_roles.append(response.json())
            # time.sleep(1)
        return parsed_roles


class UserRoleCompare():
    """Compare user roles.
    User Role model is hashing the user-role name attribute
    which allows them to converted as python set object for comparison."""

    def __init__(self, src_roles: list, trgt_roles: list) -> None:
        self.src_roles = src_roles
        self.trgt_roles = trgt_roles
        self._role_check()

    def _role_check(self):
        """User roles compare function"""
        diff_roles = set(self.src_roles).difference(set(self.trgt_roles))
        if diff_roles:
            print("\nFollowing roles are present in source but not in target:")
            for role in diff_roles:
                print(role.name)
            print()

            self._remove_diff_roles(diff_roles)
            assert (self.src_roles == self.trgt_roles), "Source & Target Roles are not same"
        print("\nNo difference in role count!")

    def _remove_diff_roles(self, diff_roles: list):
        """Remove difference in roles from src_roles list and highlight the same to user"""
        for role in diff_roles:
            try:
                self.src_roles.remove(role)
            except ValueError:
                print(f"'{role.name}' not found in source list to delete")

    def vlan_check(self):
        """Vlan source IP check"""
        for src_role in self.src_roles:
            trgt_role_index = self.trgt_roles.index(src_role) # Since both src_roles & trgt_roles are same
            # we are fetching the index of role and pop it from trgt_roles.
            trgt_role = self.trgt_roles.pop(trgt_role_index)
            if not src_role.general == trgt_role.general:
                print(f"Role:{src_role.name}")
                # print( f"Source IP: {src_role.general['vlan-source-ip']['source-ip']}")
                print(f"Source VLAN: {src_role.general['vlan-source-ip']['vlan']}")
                # print( f"Target IP: {trgt_role.general['vlan-source-ip']['source-ip']}")
                print(f"Target VLAN: {trgt_role.general['vlan-source-ip']['vlan']}")
                print()
