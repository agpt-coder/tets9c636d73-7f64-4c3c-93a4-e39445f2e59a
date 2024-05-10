import prisma
import prisma.models
from pydantic import BaseModel


class DeleteInventoryItemResponse(BaseModel):
    """
    This model provides feedback on the outcome of the delete operation. It will confirm successful deletion or provide an error message if the deletion could not be performed.
    """

    message: str


async def deleteInventoryItem(itemId: int) -> DeleteInventoryItemResponse:
    """
    Removes an inventory item from the system based on the item ID. This action is critical to maintain an up-to-date and accurate inventory record, preventing discrepancies in stock levels.

    Args:
        itemId (int): Unique identifier for the inventory item to be deleted.

    Returns:
        DeleteInventoryItemResponse: This model provides feedback on the outcome of the delete operation. It will confirm successful deletion or provide an error message if the deletion could not be performed.

    Example:
        deleteInventoryItem(10)
        > DeleteInventoryItemResponse(message="Item successfully deleted.")
    """
    try:
        item = await prisma.models.Item.prisma().find_unique(
            where={"id": itemId}, include={"inventoryEvents": True}
        )
        if item is None:
            return DeleteInventoryItemResponse(
                message=f"No inventory item found with ID {itemId}."
            )
        if len(item.inventoryEvents) > 0:
            return DeleteInventoryItemResponse(
                message="Cannot delete the item as there are related inventory events."
            )
        await prisma.models.Item.prisma().delete(where={"id": itemId})
        return DeleteInventoryItemResponse(message="Item successfully deleted.")
    except Exception as e:
        return DeleteInventoryItemResponse(message=f"Error deleting item: {str(e)}")
