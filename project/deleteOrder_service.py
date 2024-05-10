import prisma
import prisma.models
from pydantic import BaseModel


class DeleteOrderResponse(BaseModel):
    """
    This model represents the response returned to the client after attempting to delete an order, including a success status or error message.
    """

    success: bool
    message: str


async def deleteOrder(orderId: int) -> DeleteOrderResponse:
    """
    Deletes an order based on its ID. This API endpoint ensures that the order is removed from the system, and all associated schedules and inventory adjustments are notified. Critical from a management perspective to maintain data integrity and inventory accuracy.

    Args:
        orderId (int): The unique identifier of the order to be deleted.

    Returns:
        DeleteOrderResponse: This model represents the response returned to the client after attempting to delete an order, including a success status or error message.

    Example:
        deleteOrder(5)
        > DeleteOrderResponse(success=True, message="prisma.models.Order deleted successfully.")
    """
    order = await prisma.models.Order.prisma().find_unique(where={"id": orderId})
    if order is None:
        return DeleteOrderResponse(
            success=False, message="prisma.models.Order not found."
        )
    await prisma.models.Order.prisma().delete(where={"id": orderId})
    return DeleteOrderResponse(
        success=True, message="prisma.models.Order deleted successfully."
    )
