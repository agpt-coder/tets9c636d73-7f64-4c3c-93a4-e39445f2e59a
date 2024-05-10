from datetime import datetime
from typing import List

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class OrderItem(BaseModel):
    """
    Defines an item and the quantity to order.
    """

    itemId: int
    quantity: int


class CreateOrderResponse(BaseModel):
    """
    Response model for the creation of a new order. Includes confirmation and order details.
    """

    orderId: int
    confirmationStatus: str
    expectedDeliveryDate: datetime


async def createOrder(
    items: List[OrderItem], customerId: int, expectedDeliveryDate: datetime
) -> CreateOrderResponse:
    """
    Creates a new order. It accepts details like items, quantities, customer information, and expected delivery details. This endpoint interacts with the Inventory Management Module to verify stock availability and with the Scheduling Module to confirm delivery dates. Expected to return the created order details with a confirmation status.

    Args:
        items (List[OrderItem]): List of items and quantities to be ordered.
        customerId (int): The ID of the customer placing the order.
        expectedDeliveryDate (datetime): The expected date time for delivering the order.

    Returns:
        CreateOrderResponse: Response model for the creation of a new order. Includes confirmation and order details.
    """
    items_available = True
    item_shortages = []
    for item in items:
        stock_item = await prisma.models.Item.prisma().find_unique(
            where={"id": item.itemId}
        )
        if stock_item is None or stock_item.stockLevel < item.quantity:
            items_available = False
            item_shortages.append(item.itemId)
    if not items_available:
        return CreateOrderResponse(
            orderId=0,
            confirmationStatus="pending stock check due to insufficient stocks for items: "
            + ", ".join(map(str, item_shortages)),
            expectedDeliveryDate=expectedDeliveryDate,
        )
    order = await prisma.models.Order.prisma().create(
        data={
            "customerId": customerId,
            "deliveryDate": expectedDeliveryDate,
            "status": prisma.enums.OrderStatus.PLACED,
        }
    )
    line_items = [
        {"orderId": order.id, "itemId": item.itemId, "quantity": item.quantity}
        for item in items
    ]
    await prisma.models.LineItem.prisma().create_many(data=line_items)
    for item in items:
        await prisma.models.Item.prisma().update(
            where={"id": item.itemId}, data={"stockLevel": {"decrement": item.quantity}}
        )
    return CreateOrderResponse(
        orderId=order.id,
        confirmationStatus="confirmed",
        expectedDeliveryDate=expectedDeliveryDate,
    )
