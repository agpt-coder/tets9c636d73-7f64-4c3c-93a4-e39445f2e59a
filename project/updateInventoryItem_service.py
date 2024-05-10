from enum import Enum
from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class Category(Enum):
    """
    Enum representing different categories of items in inventory
    """

    value: str  # TODO(autogpt): "value" incorrectly overrides property of same name in class "Enum". reportIncompatibleMethodOverride


class UpdateInventoryItemResponse(BaseModel):
    """
    Response model for the inventory item update operation. Returns the updated inventory item details.
    """

    itemId: int
    name: str
    category: Category
    stockLevel: int
    minStockLevel: int
    reOrderNeed: bool


async def updateInventoryItem(
    itemId: int,
    quantity: Optional[int],
    condition: Optional[str],
    location: Optional[str],
) -> UpdateInventoryItemResponse:
    """
    Updates existing inventory item details based on the item ID provided. Can include updates to quantity, condition, and location.
    This function aims to update inventory data in a database, effectively reflecting its current status.

    Args:
        itemId (int): The unique identifier for the inventory item to update.
        quantity (Optional[int]): The new quantity of the inventory item, if applicable.
        condition (Optional[str]): The new condition state of the inventory item, if applicable. Not used in update as the schema lacks a field.
        location (Optional[str]): The new storage location of the inventory item, if applicable. Not used in update as the schema lacks a field.

    Returns:
        UpdateInventoryItemResponse: Response model including the updated inventory item details.
    """
    item = await prisma.models.Item.prisma().find_unique(where={"id": itemId})
    if item is None:
        raise ValueError("No item found with the given ID.")
    update_data = {}
    if quantity is not None:
        update_data["stockLevel"] = quantity
        update_data["reOrderNeed"] = quantity <= item.minStockLevel
    updated_item = await prisma.models.Item.prisma().update(
        where={"id": itemId}, data=update_data
    )
    return UpdateInventoryItemResponse(
        itemId=updated_item.id,
        name=updated_item.name,
        category=Category(updated_item.category),
        stockLevel=updated_item.stockLevel,
        minStockLevel=updated_item.minStockLevel,
        reOrderNeed=updated_item.reOrderNeed,
    )
