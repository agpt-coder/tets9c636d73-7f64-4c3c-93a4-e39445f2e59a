from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class GetCustomersRequest(BaseModel):
    """
    Request model for fetching a list of customers. There are no path or query parameters specified, so this model does not need any fields.
    """

    pass


class OrderSummary(BaseModel):
    """
    Contains minimal information about the customer's most recent order suitable for quick reference.
    """

    order_id: int
    order_amount: float


class CustomerSummary(BaseModel):
    """
    Summarized information of a customer for quick lookup purposes. Integrates latest financial status from QuickBooks.
    """

    customer_id: int
    name: str
    latest_order: OrderSummary


class GetCustomersResponse(BaseModel):
    """
    Response model for the GET /customers endpoint. Provides essential details about each customer for quick look-ups in the system.
    """

    customers: List[CustomerSummary]


async def listCustomers(request: GetCustomersRequest) -> GetCustomersResponse:
    """
    Lists all customers within the system. It provides a summary view suitable for quick look-ups and decision-making processes, offering fields like customer ID, name, and latest orders. Each entry is connected with QuickBooks to reflect the latest financial status.

    Args:
        request (GetCustomersRequest): Request model for fetching a list of customers. There are no path or query parameters specified, so this model does not need any fields.

    Returns:
        GetCustomersResponse: Response model for the GET /customers endpoint. Provides essential details about each customer for quick look-ups in the system.
    """
    all_customers = await prisma.models.Customer.prisma().find_many(
        include={
            "orders": {
                "take": 1,
                "order": {"createdDate": "desc"},
                "include": {"sale": True},
            }
        }
    )
    customers_list = []
    for customer in all_customers:
        latest_order = customer.orders[0] if customer.orders else None
        latest_order_summary = (
            OrderSummary(
                order_id=latest_order.id if latest_order else None,
                order_amount=latest_order.sale.amount
                if latest_order and latest_order.sale
                else 0,
            )
            if latest_order
            else None
        )
        customer_summary = CustomerSummary(
            customer_id=customer.id,
            name=customer.name,
            latest_order=latest_order_summary,
        )
        customers_list.append(customer_summary)
    response = GetCustomersResponse(customers=customers_list)
    return response
