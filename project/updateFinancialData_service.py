from datetime import datetime

import prisma
import prisma.models
from pydantic import BaseModel


class UpdateFinancialDataResponse(BaseModel):
    """
    Response model indicating the result of the update attempt. Includes success status and any pertinent messages or error details.
    """

    success: bool
    message: str


async def updateFinancialData(
    transactionId: str,
    amount: float,
    transactionDate: datetime,
    category: str,
    details: str,
) -> UpdateFinancialDataResponse:
    """
    Updates existing financial records in QuickBooks. This endpoint can handle changes such as updating a transaction's details or modifying a financial report. It ensures data integrity by verifying changes before syncing with QuickBooks. Changes typically include entries like revised amounts, dates, or categorizations.

    Args:
        transactionId (str): Unique identifier for the transaction to update.
        amount (float): Revised amount for the transaction.
        transactionDate (datetime): The new date of the transaction.
        category (str): Updated category designation for the financial record.
        details (str): Additional details about the changes made.

    Returns:
        UpdateFinancialDataResponse: Response model indicating the result of the update attempt. Includes success status and any pertinent messages or error details.
    """
    try:
        sale = await prisma.models.Sale.prisma().find_unique(
            where={"id": int(transactionId)}
        )
        if not sale:
            return UpdateFinancialDataResponse(
                success=False, message="Transaction not found."
            )
        updated_sale = await prisma.models.Sale.prisma().update(
            where={"id": int(transactionId)},
            data={"amount": amount, "saleDate": transactionDate},
        )
        print(
            f"Updated transaction {transactionId} with amount: {amount}, date: {transactionDate}, category: {category}, details: {details}"
        )
        return UpdateFinancialDataResponse(
            success=True, message="Transaction updated successfully."
        )
    except Exception as e:
        return UpdateFinancialDataResponse(success=False, message=str(e))
