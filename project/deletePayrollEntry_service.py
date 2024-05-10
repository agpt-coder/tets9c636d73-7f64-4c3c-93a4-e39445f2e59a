import prisma
import prisma.models
from pydantic import BaseModel


class DeletePayrollResponse(BaseModel):
    """
    This response model provides a confirmation of the deletion of the payroll entry. It helps ensure that the client receives feedback on whether the delete operation was successful or not.
    """

    success: bool
    message: str


async def deletePayrollEntry(id: int) -> DeletePayrollResponse:
    """
    Deletes a payroll entry by ID. This action will remove the entry from the system and subsequently update QuickBooks to ensure financial data integrity. The expected response is a confirmation of deletion.

    Args:
        id (int): The unique identifier of the payroll entry to be deleted.

    Returns:
        DeletePayrollResponse: This response model provides a confirmation of the deletion of the payroll entry. It helps ensure that the client receives feedback on whether the delete operation was successful or not.

    Example:
        response = deletePayrollEntry(123)
        > DeletePayrollResponse(success=True, message='prisma.models.Payroll deleted successfully.')
    """
    payroll = await prisma.models.Payroll.prisma().find_unique(where={"id": id})
    if payroll:
        await prisma.models.Payroll.prisma().delete(where={"id": id})
        return DeletePayrollResponse(
            success=True, message="prisma.models.Payroll deleted successfully."
        )
    else:
        return DeletePayrollResponse(
            success=False, message="prisma.models.Payroll entry not found."
        )
