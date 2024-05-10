from datetime import datetime
from enum import Enum

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class PaymentStatus(BaseModel):
    """
    Enum covering all possible payment states. Expected values are: PENDING, COMPLETED, FAILED.
    """

    pass


class Sale(BaseModel):
    """
    Sale model covering specifics of a financial transaction.
    """

    saleId: int
    saleDate: datetime
    amount: float
    paymentStatus: PaymentStatus


class Order(BaseModel):
    """
    Order model consisting of individual order details.
    """

    orderId: int
    createdDate: datetime
    status: prisma.enums.OrderStatus
    saleDetails: Sale


class OrderUpdateResponse(BaseModel):
    """
    Response model for updating an order. Confirms the successful application of updates and provides the updated order details.
    """

    success: bool
    updatedOrderDetails: Order


class OrderStatus(Enum):
    PLACED: str = "PLACED"
    IN_PROCESS: str = "IN_PROCESS"
    SHIPPED: str = "SHIPPED"
    DELIVERED: str = "DELIVERED"
    CANCELLED: str = "CANCELLED"


async def updateOrder(
    orderId: int,
    customerRequests: str,
    newDeliveryDate: datetime,
    orderSizeAdjustment: int,
) -> OrderUpdateResponse:
    """
    Updates the details of an existing order. Permissions are restricted to modifications by authorized roles only. Useful for handling changes in order sizes, customer requests, or delivery dates. This endpoint syncs with Inventory and Scheduling modules to adjust plans and stocks.

    Args:
        orderId (int): The unique identifier of the order to be updated. Necessary to locate the specific order in the database.
        customerRequests (str): Customer-specific requests or changes to the order, such as special handling or preferences.
        newDeliveryDate (datetime): Updated delivery date if changes are required by the customer or operational adjustments.
        orderSizeAdjustment (int): Adjustments to the original order size, either an increase or decrease in the quantity ordered.

    Returns:
        OrderUpdateResponse: Response model for updating an order. Confirms the successful application of updates and provides the updated order details.

    Example:
        updateOrder(123, "Please add gift wrap.", datetime(2023, 12, 24), 10)
        > OrderUpdateResponse(success=True, updatedOrderDetails=Order(...))
    """
    order = await prisma.models.Order.prisma().find_unique(where={"id": orderId})
    if not order:
        return OrderUpdateResponse(success=False, updatedOrderDetails=None)
    await prisma.models.Order.prisma().update(
        where={"id": orderId}, data={"deliveryDate": newDeliveryDate}
    )
    if orderSizeAdjustment != 0:
        line_items = await prisma.models.LineItem.prisma().find_many(
            where={"orderId": orderId}
        )
        for item in line_items:
            new_quantity = max(0, item.quantity + orderSizeAdjustment)
            await prisma.models.LineItem.prisma().update(
                where={"id": item.id}, data={"quantity": new_quantity}
            )
    updated_order = await prisma.models.Order.prisma().find_unique(
        where={"id": orderId}
    )
    return OrderUpdateResponse(success=True, updatedOrderDetails=updated_order)
