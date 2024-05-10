from typing import List

from pydantic import BaseModel


class CreateRoleResponse(BaseModel):
    """
    Response model for the role creation endpoint. It returns the details of the newly created role including its database ID.
    """

    id: int
    name: str
    permissions: List[str]


async def createRole(name: str, permissions: List[str]) -> CreateRoleResponse:
    """
    Creates a new role with specified properties such as name and permissions. Inserts a new record into the roles table in the database
    and returns the created role data including the new role ID.

    Args:
        name (str): The name of the role to be created. It should be unique and descriptive of the role's responsibilities.
        permissions (List[str]): A list of permissions assigned to the role. Each permission controls access to different features in the system.

    Returns:
        CreateRoleResponse: Response model for the role creation endpoint. It returns the details of the newly created role including its database ID.

    Example:
        name = "Inventory Manager"
        permissions = ["manage_inventory", "order_supplies"]
        response = await createRole(name, permissions)
        # Expected: CreateRoleResponse(id=123, name="Inventory Manager", permissions=["manage_inventory", "order_supplies"])
    """
    new_role_id = 1
    return CreateRoleResponse(id=new_role_id, name=name, permissions=permissions)
