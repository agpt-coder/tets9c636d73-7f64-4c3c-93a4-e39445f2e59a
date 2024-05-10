from datetime import datetime

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class ScheduleDeliveryResponse(BaseModel):
    """
    Model for confirming the scheduling of a delivery. Includes details about the scheduled delivery or error messages.
    """

    success: bool
    message: str
    scheduled_datetime: datetime


async def scheduleDelivery(
    delivery_date: datetime,
    quantity: int,
    destination: str,
    item_id: int,
    customer_id: int,
) -> ScheduleDeliveryResponse:
    """
    Schedules a new delivery. This endpoint takes details such as delivery date, quantity, and destination, and coordinates with the Scheduling Module to ensure transport availability.

    Args:
        delivery_date (datetime): The scheduled date for the delivery.
        quantity (int): The quantity of items to be delivered.
        destination (str): The destination address where the items will be delivered.
        item_id (int): The database ID of the item to be delivered.
        customer_id (int): The ID of the customer receiving the delivery.

    Returns:
        ScheduleDeliveryResponse: Model for confirming the scheduling of a delivery. Includes details about the scheduled delivery or error messages.

    Example:
        from datetime import datetime
        response = await scheduleDelivery(
            datetime(2023, 12, 25),
            50,
            "123 Example Lane",
            1,
            1
        )
        print(response)  # Output depends on the success or failure of delivery scheduling.
    """
    item = await prisma.models.Item.prisma().find_unique(where={"id": item_id})
    if item is None or item.stockLevel < quantity:
        return ScheduleDeliveryResponse(
            success=False,
            message="Insufficient stock for the item or item does not exist.",
            scheduled_datetime=delivery_date,
        )
    customer = await prisma.models.Customer.prisma().find_unique(
        where={"id": customer_id}
    )
    if customer is None:
        return ScheduleDeliveryResponse(
            success=False,
            message="Customer does not exist.",
            scheduled_datetime=delivery_date,
        )
    schedule = await prisma.models.Schedule.prisma().create(
        data={
            "scheduledOn": delivery_date,
            "type": prisma.enums.ScheduleType.DELIVERY.value,
            "status": prisma.enums.ScheduleStatus.PENDING.value,
        }
    )
    new_stock_level = item.stockLevel - quantity
    await prisma.models.Item.prisma().update(
        where={"id": item_id}, data={"stockLevel": new_stock_level}
    )
    order = await prisma.models.Order.prisma().create(
        data={
            "customer": {"connect": {"id": customer_id}},
            "createdDate": datetime.now(),
            "deliveryDate": delivery_date,
            "status": prisma.enums.OrderStatus.PLACED.value,
            "lineItems": {
                "create": [
                    {
                        "item": {"connect": {"id": item_id}},
                        "quantity": quantity,
                        "pricePerItem": 0.0,
                    }
                ]
            },
        }
    )
    return ScheduleDeliveryResponse(
        success=True,
        message="Delivery scheduled successfully.",
        scheduled_datetime=delivery_date,
    )
