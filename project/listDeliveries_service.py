from datetime import datetime
from enum import Enum
from typing import List, Optional

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class Category(Enum):
    """
    Enum representing different categories of items in inventory
    """

    value: str  # TODO(autogpt): "value" incorrectly overrides property of same name in class "Enum". reportIncompatibleMethodOverride


class ItemOverview(BaseModel):
    """
    Overview of an item including name, category, and quantity.
    """

    name: str
    category: Category
    quantity: int


class OrderOverview(BaseModel):
    """
    Basic details about the order linked to the delivery.
    """

    orderId: int
    customerName: str
    deliveryStatus: prisma.enums.OrderStatus


class DeliveryDetail(BaseModel):
    """
    Detailed record for each delivery, including dates, items, and order information.
    """

    scheduledDate: datetime
    itemDetails: List[ItemOverview]
    orderDetails: OrderOverview


class DeliveriesResponse(BaseModel):
    """
    Response model for the delivery list output, representing comprehensive delivery schedules including items, orders, and scheduled details.
    """

    deliveries: List[DeliveryDetail]


class ScheduleStatus(Enum):
    PENDING: str = "PENDING"
    COMPLETED: str = "COMPLETED"
    CANCELLED: str = "CANCELLED"


async def listDeliveries(
    startDate: datetime,
    endDate: datetime,
    status: ScheduleStatus,
    itemCategory: Optional[Category],
) -> DeliveriesResponse:
    schedules = await prisma.models.Schedule.prisma().find_many(
        where={
            "scheduledOn": {"gte": startDate, "lte": endDate},
            "status": status,
            "type": prisma.enums.ScheduleType.DELIVERY,
        },
        include={
            "user": True,
            "orders": {"include": {"lineItems": {"include": {"item": True}}}},
        },
    )
    delivery_details_list = []
    for schedule in schedules:
        for (
            order
        ) in (
            schedule.orders
        ):  # TODO(autogpt): Cannot access member "orders" for type "Schedule"
            #     Member "orders" is unknown. reportAttributeAccessIssue
            for line_item in order.lineItems:
                if itemCategory is None or line_item.item.category == itemCategory:
                    item_overview = ItemOverview(
                        name=line_item.item.name,
                        category=line_item.item.category,
                        quantity=line_item.quantity,
                    )
                    order_overview = OrderOverview(
                        orderId=order.id,
                        customerName=order.customer.name,
                        deliveryStatus=order.status,
                    )
                    delivery_detail = DeliveryDetail(
                        scheduledDate=schedule.scheduledOn,
                        itemDetails=[item_overview],
                        orderDetails=order_overview,
                    )
                    delivery_details_list.append(delivery_detail)
    return DeliveriesResponse(deliveries=delivery_details_list)
