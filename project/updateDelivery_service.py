from datetime import datetime
from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class UpdatedQuantity(BaseModel):
    """
    Represents an updated quantity for a specific item in the delivery.
    """

    itemId: int
    quantity: int


class ItemQuantity(BaseModel):
    """
    Details of a specific item and its quantity in the delivery.
    """

    itemId: int
    quantity: int


class DeliveryDetails(BaseModel):
    """
    Contains detailed information of a scheduled delivery after updates.
    """

    deliveryId: int
    scheduledDate: datetime
    itemQuantities: List[ItemQuantity]


class UpdateDeliveryDetailsResponse(BaseModel):
    """
    Provides feedback on the successful or failed update of delivery details.
    """

    success: bool
    message: str
    updatedDelivery: DeliveryDetails


async def updateDelivery(
    deliveryId: int, newDeliveryDate: datetime, updatedQuantities: List[UpdatedQuantity]
) -> UpdateDeliveryDetailsResponse:
    """
    Updates specifics of a scheduled delivery. General adjustments include changing delivery dates or quantities, which are synchronized with updates in the Scheduling and Inventory Management Modules.

    Args:
        deliveryId (int): The unique identifier of the delivery to be updated.
        newDeliveryDate (datetime): The new intended delivery date.
        updatedQuantities (List[UpdatedQuantity]): A list of new quantities per item for this delivery.

    Returns:
        UpdateDeliveryDetailsResponse: Provides feedback on the successful or failed update of delivery details.
    """
    delivery = await prisma.models.Order.prisma().update(
        where={"id": deliveryId}, data={"deliveryDate": newDeliveryDate}
    )
    if not delivery:
        return UpdateDeliveryDetailsResponse(
            success=False,
            message="Failed to update delivery date. Check delivery ID.",
            updatedDelivery=None,
        )
    for update in updatedQuantities:
        await prisma.models.LineItem.prisma().update_many(
            where={"orderId": deliveryId, "itemId": update.itemId},
            data={"quantity": update.quantity},
        )
    updated_items = [
        ItemQuantity(itemId=update.itemId, quantity=update.quantity)
        for update in updatedQuantities
    ]
    updated_delivery_details = DeliveryDetails(
        deliveryId=delivery.id,
        scheduledDate=newDeliveryDate,
        itemQuantities=updated_items,
    )
    return UpdateDeliveryDetailsResponse(
        success=True,
        message="Delivery updated successfully.",
        updatedDelivery=updated_delivery_details,
    )
