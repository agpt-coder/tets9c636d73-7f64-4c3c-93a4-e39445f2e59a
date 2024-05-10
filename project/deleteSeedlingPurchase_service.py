import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class DeleteSeedlingPurchaseResponse(BaseModel):
    """
    Response model indicating successful deletion of a seedling purchase and adjustment of inventory levels.
    """

    success: bool
    message: str


async def deleteSeedlingPurchase(purchaseId: int) -> DeleteSeedlingPurchaseResponse:
    """
    Deletes a seedling purchase record. This operation will also decrease the corresponding items in Inventory, ensuring that the stock levels are accurate post-deletion.

    Args:
        purchaseId (int): The unique identifier for the seedling purchase to be deleted.

    Returns:
        DeleteSeedlingPurchaseResponse: Response model indicating successful deletion of a seedling purchase and adjustment of inventory levels.
    """
    try:
        line_item = await prisma.models.LineItem.prisma().find_unique(
            where={"id": purchaseId}, include={"item": True}
        )
        if line_item is None:
            return DeleteSeedlingPurchaseResponse(
                success=False, message="No seedling purchase found with this ID."
            )
        updated_item = await prisma.models.Item.prisma().update(
            where={"id": line_item.itemId},
            data={"stockLevel": {"decrement": line_item.quantity}},
        )
        await prisma.models.InventoryEvent.prisma().create(
            {
                "data": {
                    "itemId": line_item.itemId,
                    "eventType": prisma.enums.InventoryEventType.ADJUSTED,
                    "quantityChange": -line_item.quantity,
                }
            }
        )
        await prisma.models.LineItem.prisma().delete(where={"id": purchaseId})
        return DeleteSeedlingPurchaseResponse(
            success=True,
            message="Seedling purchase deleted and inventory updated successfully.",
        )
    except Exception as e:
        return DeleteSeedlingPurchaseResponse(
            success=False, message=f"Error during deletion: {str(e)}"
        )
