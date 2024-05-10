from datetime import datetime
from typing import List, Optional

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class Customer(BaseModel):
    """
    Customer entity with contact details.
    """

    name: str
    email: str
    contactNumber: Optional[str] = None


class Item(BaseModel):
    """
    Details about each item within the order.
    """

    name: str
    quantity: int
    pricePerItem: float


class Schedule(BaseModel):
    """
    Schedule entity, denoting the planned activities like delivery.
    """

    scheduledOn: datetime
    type: prisma.enums.ScheduleType
    status: prisma.enums.ScheduleStatus


class OrderDetailsResponse(BaseModel):
    """
    This model captures the detailed information about an order, including customer details, list of items, order status, and delivery schedule.
    """

    orderId: int
    customer: Customer
    items: List[Item]
    status: prisma.enums.OrderStatus
    scheduledDelivery: Schedule


async def getOrder(orderId: int) -> OrderDetailsResponse:
    """
    Retrieves detailed information about a specific order using its ID. This information includes
    customer details, item list, order status, and delivery schedule. Useful for prisma.models.Order Managers
    and Sales Managers to track the order status and update customers.

    Args:
        orderId (int): The unique identifier of the order to retrieve detailed information for.

    Returns:
        OrderDetailsResponse: This model captures the detailed information about an order,
        including customer details, list of items, order status, and delivery schedule.
    """
    order = await prisma.models.Order.prisma().find_first(
        where={"id": orderId},
        include={
            "customer": True,
            "lineItems": {"include": {"item": True}},
            "user": {"include": {"schedules": True}},
        },
    )
    if not order:
        raise ValueError(f"No order found with ID {orderId}")
    if (
        not order.customer
        or not order.lineItems
        or (not order.user)
        or (not order.user.schedules)
    ):
        raise ValueError("prisma.models.Order data is incomplete.")
    customer = Customer(
        name=order.customer.name,
        email=order.customer.email,
        contactNumber=order.customer.contactNumber,
    )
    items = [
        Item(name=li.item.name, quantity=li.quantity, pricePerItem=li.pricePerItem)
        for li in order.lineItems
        if li.item
    ]
    delivery_schedule = next(
        (
            sch
            for sch in order.user.schedules
            if sch.type == prisma.enums.ScheduleType.DELIVERY
            and sch.status != prisma.enums.ScheduleStatus.CANCELLED
        ),
        None,
    )
    if not delivery_schedule:
        scheduled_delivery = Schedule(
            scheduledOn=datetime.now(),
            type=prisma.enums.ScheduleType.DELIVERY,
            status=prisma.enums.ScheduleStatus.PENDING,
        )
    else:
        scheduled_delivery = Schedule(
            scheduledOn=delivery_schedule.scheduledOn,
            type=delivery_schedule.type,
            status=delivery_schedule.status,
        )
    return OrderDetailsResponse(
        orderId=orderId,
        customer=customer,
        items=items,
        status=order.status,
        scheduledDelivery=scheduled_delivery,
    )
