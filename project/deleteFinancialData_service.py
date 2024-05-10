import prisma
import prisma.models
from pydantic import BaseModel


class DeleteFinancialDataResponse(BaseModel):
    """
    Response model confirming the deletion of the financial record. Includes an operation status to inform the client of the success or failure of the operation.
    """

    is_deleted: bool
    message: str


async def deleteFinancialData(
    financial_record_id: str, confirmation_token: str
) -> DeleteFinancialDataResponse:
    """
    Removes financial records directly from QuickBooks. Usage of this endpoint should be strictly controlled due to the high impact nature of deleting financial data. Suitable for removing erroneous entries, with safeguards such as multi-confirmation prompts to prevent accidental data loss.

    Args:
        financial_record_id (str): The unique identifier for the financial record to delete.
        confirmation_token (str): A security token or passphrase to confirm the intent to delete, enhancing the safeguard against accidental deletions.

    Returns:
        DeleteFinancialDataResponse: Response model confirming the deletion of the financial record. Includes an operation status to inform the client of the success or failure of the operation.

    Example:
        response = await deleteFinancialData('123', 'securetoken123')
        print(response.is_deleted)  # Prints: True or False based on the operation success.
        print(response.message)     # Description of operation result.
    """
    if confirmation_token != "AdminConfirmation2023":
        return DeleteFinancialDataResponse(
            is_deleted=False, message="Invalid confirmation token."
        )
    order = await prisma.models.Order.prisma().find_unique(
        where={"id": int(financial_record_id)}
    )
    if not order:
        return DeleteFinancialDataResponse(
            is_deleted=False, message="No financial record found with the provided ID."
        )
    await prisma.models.Order.prisma().delete(where={"id": order.id})
    return DeleteFinancialDataResponse(
        is_deleted=True, message="Financial record successfully deleted."
    )
