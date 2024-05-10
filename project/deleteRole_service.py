import prisma
import prisma.models
from pydantic import BaseModel


class DeleteRoleResponse(BaseModel):
    """
    A confirmation response that indicates whether the role was successfully deleted.
    """

    success: bool


async def deleteRole(roleId: int) -> DeleteRoleResponse:
    """
    Removes a staff role from the system using the roleId specified. This performs a lookup to ensure the role
    exists, deletes it from the database, and confirms the deletion with a success response. This is essential
    for managing outdated or unnecessary roles.

    Args:
        roleId (int): The unique identifier of the role to be deleted.

    Returns:
        DeleteRoleResponse: A confirmation response that indicates whether the role was successfully deleted.

    Example:
        response = await deleteRole(1)
        > {'success': True}
    """
    role = await prisma.models.User.prisma().find_first(
        where={"role": {"equals": roleId}}
    )
    if role is None:
        return DeleteRoleResponse(success=False)
    await prisma.models.User.prisma().delete_many(where={"role": {"equals": roleId}})
    role_check = await prisma.models.User.prisma().find_first(
        where={"role": {"equals": roleId}}
    )
    return DeleteRoleResponse(success=role_check is None)
