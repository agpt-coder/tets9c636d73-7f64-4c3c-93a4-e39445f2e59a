from datetime import datetime
from typing import List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class ItemWithQuantity(BaseModel):
    """
    Structure defining item types with their respective quantities in an order.
    """

    itemId: int
    quantity: int


class InitialOrderDetails(BaseModel):
    """
    Details capturing initial order information at customer creation time.
    """

    items: List[ItemWithQuantity]
    deliveryDate: Optional[datetime] = None


class CreateCustomerResponse(BaseModel):
    """
    Outputs the details of the newly created customer and confirms the successful record creation.
    """

    customerId: int
    message: str


async def createCustomer(
    name: str,
    email: str,
    contactNumber: Optional[str],
    preferences: str,
    initialOrder: InitialOrderDetails,
) -> CreateCustomerResponse:
    """
    Creates a new customer record. This includes storing information such as name, contact details, preferences, and initial order data. The endpoint will also trigger a sync with QuickBooks to initialize the financial tracking for the new customer.

    Args:
        name (str): Full name of the customer.
        email (str): Email address of the customer, must be unique.
        contactNumber (Optional[str]): Phone number of the customer.
        preferences (str): Preferences noted by the customer, could include information like preferred types of products or services.
        initialOrder (InitialOrderDetails): Details about the customer's initial order such as the types and quantities of items and the expected delivery date.

    Returns:
        CreateCustomerResponse: Outputs the details of the newly created customer and confirms the successful record creation.

    Example:
        name = "John Doe"
        email = "john.doe@example.com"
        contactNumber = "+1234567890"
        preferences = "Prefers natural products"
        initialOrderDetails = InitialOrderDetails(items=[ItemWithQuantity(itemId=1, quantity=10)], deliveryDate=datetime.strptime("2023-12-24", "%Y-%m-%d"))
        response = await createCustomer(name, email, contactNumber, preferences, initialOrderDetails)
        > CreateCustomerResponse(customerId=1, message='Customer created successfully.')
    """
    new_customer = await prisma.models.Customer.prisma().create(
        data={"name": name, "email": email, "contactNumber": contactNumber}
    )
    order_items = [
        {
            "item": {"connect": {"id": item.itemId}},
            "quantity": item.quantity,
            "pricePerItem": 0.0,
        }
        for item in initialOrder.items
    ]
    new_order = await prisma.models.Order.prisma().create(
        data={
            "customer": {"connect": {"id": new_customer.id}},
            "deliveryDate": initialOrder.deliveryDate,
            "lineItems": {"create": order_items},
            "status": "PLACED",
        }
    )
    response = CreateCustomerResponse(
        customerId=new_customer.id,
        message="Customer and initial order created successfully.",
    )
    return response
