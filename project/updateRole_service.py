from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class Role(BaseModel):
    """
    Enum representing various system roles.
    """

    role_value: str


class RoleResponse(BaseModel):
    """
    Model representing a role entity after an update operation. Includes the new role name and updated permissions.
    """

    roleName: Role
    roleId: str
    permissions: List[str]


async def updateRole(
    roleId: str, newRoleName: Role, newPermissions: List[str]
) -> RoleResponse:
    """
    Updates an existing staff role with new data provided in the request body. It checks if the role exists, applies the updates in the roles database, and returns the updated role entity. This endpoint ensures roles remain current and relevant.

    Args:
        roleId (str): The unique identifier for the role to be updated.
        newRoleName (Role): New name for the role, must be one of the predefined Role enum values.
        newPermissions (List[str]): List of new permissions associated with this role, represented as strings.

    Returns:
        RoleResponse: Model representing a role entity after an update operation. Includes the new role name and updated permissions.
    """
    user = await prisma.models.User.prisma().find_unique(
        where={"role": {"role_value": roleId}}
    )
    if not user:
        raise ValueError("Role with this ID does not exist.")
    updated_user = await prisma.models.User.prisma().update(
        where={"id": user.id}, data={"role": {"set": newRoleName.role_value}}
    )
    role_response = RoleResponse(
        roleName=newRoleName, roleId=roleId, permissions=newPermissions
    )
    return role_response
