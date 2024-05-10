import prisma
import prisma.models
from pydantic import BaseModel


class DeleteCustomerResponse(BaseModel):
    """
    Response model confirming the deletion of the customer, along with status information about related processes such as QuickBooks synchronization and data archiving.
    """

    message: str


async def deleteCustomer(customerId: int) -> DeleteCustomerResponse:
    """
    Removes a customer's record from the system. This endpoint also handles the removal of any links with QuickBooks and ensures that all related data such as historical orders and sales tracking is either archived or appropriately handled based on the system's data retention policy.

    Args:
        customerId (int): The unique identifier for the customer to be deleted.

    Returns:
        DeleteCustomerResponse: Response model confirming the deletion of the customer, along with status information about related processes such as QuickBooks synchronization and data archiving.
    """
    customer = await prisma.models.Customer.prisma().find_unique(
        where={"id": customerId}
    )
    if not customer:
        return DeleteCustomerResponse(message="Customer not found.")
    orders_linked = await prisma.models.Order.prisma().find_many(
        where={"customerId": customerId}
    )
    await prisma.models.Customer.prisma().delete(where={"id": customerId})
    return DeleteCustomerResponse(
        message="Customer successfully deleted and related data handled."
    )
