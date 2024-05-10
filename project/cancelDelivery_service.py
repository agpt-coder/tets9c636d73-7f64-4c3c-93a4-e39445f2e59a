import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class CancelDeliveryResponse(BaseModel):
    """
    Response after attempting to cancel a delivery. Includes success status and any related messages or data.
    """

    success: bool
    message: str


async def cancelDelivery(deliveryId: int) -> CancelDeliveryResponse:
    """
    Cancels a previously scheduled delivery. This operation triggers updates in the Scheduling Module to free up transport resources and notify the Inventory to adjust stock reserved for this delivery.

    Args:
        deliveryId (int): The unique identifier for the delivery that is to be cancelled.

    Returns:
        CancelDeliveryResponse: Response after attempting to cancel a delivery. Includes success status and any related messages or data.
    """
    schedule = await prisma.models.Schedule.prisma().find_unique(
        where={"id": deliveryId}
    )
    if schedule is None or schedule.type != prisma.enums.ScheduleType.DELIVERY:
        return CancelDeliveryResponse(
            success=False, message=f"No delivery schedule found with ID {deliveryId}."
        )
    if schedule.status in [
        prisma.enums.ScheduleStatus.COMPLETED,
        prisma.enums.ScheduleStatus.CANCELLED,
    ]:
        return CancelDeliveryResponse(
            success=False, message="Delivery is already completed or cancelled."
        )
    updated_schedule = await prisma.models.Schedule.prisma().update(
        where={"id": deliveryId}, data={"status": prisma.enums.ScheduleStatus.CANCELLED}
    )
    orders_linked_to_schedule = await prisma.models.Order.prisma().find_many(
        where={"id": schedule.userId}
    )
    for order in orders_linked_to_schedule:
        line_items = await prisma.models.LineItem.prisma().find_many(
            where={"orderId": order.id}
        )
        for item in line_items:
            await prisma.models.InventoryEvent.prisma().create(
                data={
                    "itemId": item.itemId,
                    "eventType": prisma.enums.InventoryEventType.ADJUSTED,
                    "quantityChange": item.quantity,
                }
            )
    return CancelDeliveryResponse(
        success=True,
        message="Delivery has been successfully cancelled and inventory updated.",
    )
