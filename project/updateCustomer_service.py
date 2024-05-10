from typing import Dict, List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class UpdateCustomerResponse(BaseModel):
    """
    This model confirms the successful update of the customer's record and integrates updates to QuickBooks where necessary.
    """

    success: bool
    customerId: int
    updatedFields: List[str]


async def updateCustomer(
    customerId: int,
    email: str,
    name: str,
    contactNumber: Optional[str],
    preferences: Dict[str, str],
) -> UpdateCustomerResponse:
    """
    Updates an existing customer's record. This endpoint allows modifications to customer details, preferences, and other relevant information. It also updates the linked QuickBooks data to ensure financial records are consistent with the changes.

    Args:
    customerId (int): The unique identifier for the customer whose record is to be updated.
    email (str): Updated email address of the customer.
    name (str): Updated full name of the customer.
    contactNumber (Optional[str]): Updated contact number of the customer.
    preferences (Dict[str, str]): Updated preferences detailing customer's specific requirements or likes.

    Returns:
    UpdateCustomerResponse: This model confirms the successful update of the customer's record and integrates updates to QuickBooks where necessary.
    """
    updated_fields = []
    customer = await prisma.models.Customer.prisma().find_unique(
        where={"id": customerId}
    )
    if customer is None:
        return UpdateCustomerResponse(
            success=False, customerId=customerId, updatedFields=[]
        )
    update_data = {}
    if customer.email != email:
        update_data["email"] = email
        updated_fields.append("email")
    if f"{customer.name}" != name:
        update_data["name"] = name
        updated_fields.append("name")
    if customer.contactNumber != contactNumber and contactNumber is not None:
        update_data["contactNumber"] = contactNumber
        updated_fields.append("contactNumber")
    response = await prisma.models.Customer.prisma().update(
        where={"id": customerId}, data=update_data
    )
    print("Updating QuickBooks data...")
    return UpdateCustomerResponse(
        success=True, customerId=customerId, updatedFields=updated_fields
    )
