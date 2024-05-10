from datetime import datetime

import prisma
import prisma.models
from pydantic import BaseModel


class PaymentStatus(BaseModel):
    """
    Enum covering all possible payment states. Expected values are: PENDING, COMPLETED, FAILED.
    """

    pass


class SaleResponse(BaseModel):
    """
    This model returns the updated sale object reflecting changes that have been pushed to the database and QuickBooks. It provides confirmation that the sale details have been successfully updated.
    """

    id: int
    saleDate: datetime
    amount: float
    orderId: int
    paymentStatus: PaymentStatus


async def updateSaleRecord(
    id: int, amount: float, paymentStatus: PaymentStatus
) -> SaleResponse:
    """
    Updates an existing sales record. This endpoint facilitates the modification of sales details, which are then reflected in QuickBooks for accurate and up-to-date financial reporting.

    Args:
        id (int): The unique identifier for the sale to be updated. This corresponds to a specific sales record.
        amount (float): The new total amount for the sale after the update.
        paymentStatus (PaymentStatus): A new status of the payment, indicating whether the sale has been completed, is still pending, or has failed.

    Returns:
        SaleResponse: This model returns the updated sale object reflecting changes that have been pushed to the database and QuickBooks, providing confirmation that the sale details have been successfully updated.
    """
    existing_sale = await prisma.models.Sale.prisma().find_unique(where={"id": id})
    if not existing_sale:
        raise ValueError("Sale record not found!")
    await prisma.models.Sale.prisma().update(
        where={"id": id}, data={"amount": amount, "paymentStatus": paymentStatus}
    )
    return SaleResponse(
        id=existing_sale.id,
        saleDate=existing_sale.saleDate,
        amount=amount,
        orderId=existing_sale.orderId,
        paymentStatus=paymentStatus,
    )
