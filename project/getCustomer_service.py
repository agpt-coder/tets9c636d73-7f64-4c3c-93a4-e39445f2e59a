from datetime import datetime
from typing import List

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


class CustomerDetailsResponse(BaseModel):
    """
    Provides comprehensive information about the customer, including their preference settings, full order history, and sales data pulled from QuickBooks.
    """

    id: int
    name: str
    email: str
    contactNumber: str
    orderHistory: List[Order]


async def getCustomer(customerId: str) -> CustomerDetailsResponse:
    """
    Retrieves detailed information about a specific customer by their unique ID. This includes customer preferences,
    order history, and linked QuickBooks data. It would utilize data from the Sales Tracking Module to provide a complete
    sales history and interactions from the Order Management Module to display recent order statuses.

    Args:
        customerId (str): The unique identifier of the customer whose details are being retrieved.

    Returns:
        CustomerDetailsResponse: Provides comprehensive information about the customer, including their preference settings,
        full order history, and sales data pulled from QuickBooks.
    """
    customer = await prisma.models.Customer.prisma().find_unique(
        where={"id": int(customerId)}, include={"orders": {"include": {"sale": True}}}
    )
    if not customer:
        raise ValueError("No customer found with the provided ID.")
    order_history = [
        Order(
            orderId=order.id,
            createdDate=order.createdDate,
            status=order.status.name,
            saleDetails=Sale(
                saleId=order.sale.id if order.sale else None,
                saleDate=order.sale.saleDate if order.sale else None,
                amount=order.sale.amount if order.sale else None,
                paymentStatus=order.sale.paymentStatus.name if order.sale else None,
            ),
        )
        for order in customer.orders
        if order.sale
    ]
    customer_details = CustomerDetailsResponse(
        id=customer.id,
        name=customer.name,
        email=customer.email,
        contactNumber=customer.contactNumber if customer.contactNumber else "N/A",
        orderHistory=order_history,
    )
    return customer_details
