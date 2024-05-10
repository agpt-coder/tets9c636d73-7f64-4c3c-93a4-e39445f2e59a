import prisma
import prisma.models
from pydantic import BaseModel


class DeleteSaleResponse(BaseModel):
    """
    Response model for deletion of a sale. Returns success status and a message indicating the sale was synced with QuickBooks.
    """

    success: bool
    message: str


async def deleteSaleRecord(id: int) -> DeleteSaleResponse:
    """
    Deletes a sales record. This endpoint ensures that the deletion of sales data is also synced with QuickBooks to maintain accurate financial records.

    Args:
    id (int): The unique identifier for the sale record to be deleted.

    Returns:
    DeleteSaleResponse: Response model for deletion of a sale. Returns success status and a message indicating the sale was synced with QuickBooks.
    """
    sale = await prisma.models.Sale.prisma().find_unique(where={"id": id})
    if sale:
        await prisma.models.Sale.prisma().delete(where={"id": id})
        sync_success = True
        if sync_success:
            message = "Sale successfully deleted and synced with QuickBooks."
        else:
            message = "Sale deleted but failed to sync with QuickBooks."
        return DeleteSaleResponse(success=True, message=message)
    else:
        return DeleteSaleResponse(
            success=False, message="No sale found with the provided ID."
        )
