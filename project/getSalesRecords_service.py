from datetime import datetime
from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class GetSalesRequest(BaseModel):
    """
    Request model for fetching all sales records. No specific input parameters are needed.
    """

    pass


class PaymentStatus(BaseModel):
    """
    Enum covering all possible payment states. Expected values are: PENDING, COMPLETED, FAILED.
    """

    pass


class SaleModel(BaseModel):
    """
    A model representing a sale with all relevant details extracted from the 'Sale' database table schema.
    """

    id: int
    saleDate: datetime
    amount: float
    orderId: int
    paymentStatus: PaymentStatus


class GetSalesResponse(BaseModel):
    """
    Response model containing a list of all sales records for the organization, detailed with fields deriving from the 'Sale' database model.
    """

    sales: List[SaleModel]


async def getSalesRecords(request: GetSalesRequest) -> GetSalesResponse:
    """
    Retrieves all sales records. This endpoint provides a comprehensive view of the sales data for reporting and analysis, supporting integration with QuickBooks for financial management and reporting.

    Args:
        request (GetSalesRequest): Request model for fetching all sales records. No specific input parameters are needed.

    Returns:
        GetSalesResponse: Response model containing a list of all sales records for the organization, detailed with fields deriving from the 'Sale' database model.
    """
    sales_records = await prisma.models.Sale.prisma().find_many()
    sales_list = [
        SaleModel(
            id=sale.id,
            saleDate=sale.sale_date,
            amount=sale.amount,
            orderId=sale.order_id,
            paymentStatus=sale.payment_status.name,
        )
        for sale in sales_records
    ]  # TODO(autogpt): Cannot access member "sale_date" for type "Sale"
    #     Member "sale_date" is unknown. reportAttributeAccessIssue
    return GetSalesResponse(sales=sales_list)
