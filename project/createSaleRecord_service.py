from datetime import datetime

import prisma
import prisma.models
from pydantic import BaseModel


class PaymentStatus(BaseModel):
    """
    Enum covering all possible payment states. Expected values are: PENDING, COMPLETED, FAILED.
    """

    pass


class CreateSaleOutput(BaseModel):
    """
    Output model for the POST sales record creation, definitively confirms the sale details and payment status.
    """

    id: int
    amount: float
    saleDate: datetime
    orderId: int
    paymentStatus: PaymentStatus


async def createSaleRecord(
    amount: float, saleDate: datetime, orderId: int, paymentStatus: PaymentStatus
) -> CreateSaleOutput:
    """
    Creates a new sales record in the database, capturing sale details including the order linked to it and the payment status.
    This uses `prisma.models.Sale` to store the sale information directly.

    Args:
        amount (float): Total amount for the sale.
        saleDate (datetime): Date when the sale was made. If not specified, the current server datetime is used.
        orderId (int): Identifier for the associated order which tracks the items sold.
        paymentStatus (PaymentStatus): Current payment status for the sale, linked with the QuickBooks integration.

    Returns:
        CreateSaleOutput: Output model which definitively confirms the sale details and payment status.

    Raises:
        ValueError: If the `orderId` does not correspond to any existing order in the database.
    """
    order = await prisma.models.Order.prisma().find_unique(where={"id": orderId})
    if order is None:
        raise ValueError("Order with the specified ID does not exist.")
    sale = await prisma.models.Sale.prisma().create(
        data={
            "saleDate": saleDate,
            "amount": amount,
            "orderId": orderId,
            "paymentStatus": paymentStatus,
        }
    )
    return CreateSaleOutput(
        id=sale.id,
        amount=sale.amount,
        saleDate=sale.saleDate,
        orderId=sale.orderId,
        paymentStatus=sale.paymentStatus,
    )
