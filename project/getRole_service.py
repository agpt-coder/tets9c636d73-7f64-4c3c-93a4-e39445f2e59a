import prisma
import prisma.models
from pydantic import BaseModel


class RoleDetailsResponse(BaseModel):
    """
    This model provides detailed information about the staff role fetched using the role ID.
    """

    id: str
    name: str
    description: str


async def getRole(roleId: str) -> RoleDetailsResponse:
    """
    Fetches details for a specific staff role identified by roleId. This involves retrieving the role from the database by ID and returning it as JSON. It is crucial for editing roles or detailed viewing.

    Args:
        roleId (str): Unique identifier for the staff role. Used to retrieve detailed information about the role.

    Returns:
        RoleDetailsResponse: This model provides detailed information about the staff role fetched using the role ID.

    Example:
        result = await getRole('SALES_MANAGER')
        print(result)
        > RoleDetailsResponse(id='SALES_MANAGER', name='Sales Manager', description='Handles all sales operations and management of sales teams.')
    """
    role_record = await prisma.models.User.prisma().find_first(where={"role": roleId})
    if not role_record or not role_record.role:
        raise ValueError(f"Role with ID {roleId} not found")
    descriptions = {
        "SYSTEM_ADMINISTRATOR": "Manages system-wide settings and configurations.",
        "INVENTORY_MANAGER": "Oversees inventory levels and supply chain operations.",
        "SALES_MANAGER": "Handles all sales operations and management of sales teams.",
        "FIELD_MANAGER": "Responsible for the management and condition of the field operations.",
        "ORDER_MANAGER": "Ensures all orders are processed and delivered on time.",
        "HEALTH_SPECIALIST": "Monitors and manages the health of the trees and plants.",
        "HR_MANAGER": "Manages all HR related activities including staff roles and performance.",
        "FINANCIAL_MANAGER": "Handles all financial aspects related to the farm management.",
    }
    role_description = descriptions.get(roleId, "No description available.")
    role_details = RoleDetailsResponse(
        id=roleId, name=role_record.role, description=role_description
    )
    return role_details
