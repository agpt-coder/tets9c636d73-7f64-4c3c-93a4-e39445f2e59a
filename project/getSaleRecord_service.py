from datetime import datetime

import prisma
import prisma.models
from pydantic import BaseModel


class PaymentStatus(BaseModel):
    """
    Enum covering all possible payment states. Expected values are: PENDING, COMPLETED, FAILED.
    """

    pass


class GetSaleResponse(BaseModel):
    """
    Contains details of a sale record. Safe and effective representation of sales information accessed directly via the sales ID.
    """

    id: int
    saleDate: datetime
    amount: float
    paymentStatus: PaymentStatus


async def getSaleRecord(id: int) -> GetSaleResponse:
    """
    Fetches a single sales record by ID. Useful for reviewing specific transactions or audits, ensuring data consistency and accuracy through direct QuickBooks integration.

    Args:
        id (int): The unique identifier of the sales record. This is a path parameter provided in the URL.

    Returns:
        GetSaleResponse: Contains details of a sale record. Safe and effective representation of sales information accessed directly via the sales ID.
    """
    sale_record = await prisma.models.Sale.prisma().find_unique(where={"id": id})
    if sale_record is None:
        raise ValueError(f"Sasales record with ID {id} not found.")
    return GetSaleResponse(
        id=sale_record.id,
        saleDate=sale_record.saleDate,
        amount=sale_record.amount,
        paymentStatus=sale_record.paymentStatus,
    )
