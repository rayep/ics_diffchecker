"""Models - ICS Role"""

from dataclasses import dataclass, field


# def resolve_hyphen(data: dict):
#     """Change hyphen in key to underscore"""
#     return {key.replace('-', '_'): value for key, value in data.items()}


# def resolve_underscore(data: dict):
#     """Change underscore in key to hyphen"""
#     return {key.replace('_', '-'): value for key, value in data.items()}


@dataclass(unsafe_hash=True)
class UserRole():
    """User Role dataclass"""
    name: str = field(hash=True)
    general: dict = field(default_factory=dict, hash=False)


class UserRoleModel():
    """Create Role object"""

    def __init__(self, roles: list = None) -> None:
        self.roles = roles

    def create(self, roles: list = None):
        """Create User role model"""
        if (not self.roles and not roles):
            raise TypeError(
                "Please provide user roles output for model creation")
        roles = roles if roles else self.roles
        role_models = []
        for role in roles:
            vlan_config = {
                'vlan-source-ip': role['general']['vlan-source-ip']}
            role_models.append(
                UserRole(name=role['name'], general=vlan_config))
        return role_models
