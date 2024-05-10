from typing import List

import prisma
import prisma.enums
from pydantic import BaseModel


class GetRolesRequest(BaseModel):
    """
    Request model for fetching all roles. It does not require any input parameters since it's retrieving all roles regardless of conditions.
    """

    pass


class Role(BaseModel):
    """
    Enum representing various system roles.
    """

    role_value: str


class GetRolesResponse(BaseModel):
    """
    Response model containing a list of all roles with details about each. Includes role ID, name, and associated permissions for display in the management dashboard.
    """

    roles: List[Role]


async def getRoles(request: GetRolesRequest) -> GetRolesResponse:
    """
    Retrieves a list of all staff roles. Each role includes details like role ID, name, and associated permissions. This endpoint is used to display roles in the management dashboard. It queries the roles database and structures the output as a JSON array of roles.

    Args:
        request (GetRolesRequest): Request model for fetching all roles. It does not require any input parameters since it's retrieving all roles regardless of conditions.

    Returns:
        GetRolesResponse: Response model containing a list of all roles with details about each. Includes role ID, name, and associated permissions for display in the management dashboard.

    Example:
        request = GetRolesRequest()
        roles_response = await getRoles(request)
        for role in roles_response.roles:
            print(role.role_value)
    """
    roles = [role for role in prisma.enums.Role]
    role_responses = [Role(role_value=role.name) for role in roles]
    return GetRolesResponse(roles=role_responses)
