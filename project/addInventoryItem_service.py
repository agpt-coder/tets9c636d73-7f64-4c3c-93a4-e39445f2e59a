from datetime import datetime
from enum import Enum

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class Category(Enum):
    """
    Enum representing different categories of items in inventory
    """

    value: str  # TODO(autogpt): "value" incorrectly overrides property of same name in class "Enum". reportIncompatibleMethodOverride


class CreateInventoryItemResponse(BaseModel):
    """
    Confirms the addition of a new inventory item with its details or provides error information.
    """

    success: bool
    message: str
    itemId: int


async def addInventoryItem(
    name: str,
    quantity: int,
    category: Category,
    acquisitionDate: datetime,
    supplierName: str,
    supplierContact: str,
    minStockLevel: int,
) -> CreateInventoryItemResponse:
    """
    Allows the addition of a new inventory item to the database. The request should include item type, quantity, supplier details, and acquisition date.
    This endpoint ensures that new stock entries are uniformly documented.

    Args:
        name (str): Name or type of the inventory item.
        quantity (int): The quantity of the item being added.
        category (Category): Category of the item, must be one from the predefined categories in the database.
        acquisitionDate (datetime): The date when the item was acquired.
        supplierName (str): Name of the supplier providing the item.
        supplierContact (str): Contact details of the supplier.
        minStockLevel (int): Minimum stock level to maintain for this item before a reorder is necessary.

    Returns:
        CreateInventoryItemResponse: Confirms the addition of a new inventory item with its details or provides error information.
    """
    category_name = category.value
    try:
        item = await prisma.models.Item.prisma().create(
            data={
                "name": name,
                "category": category_name,
                "stockLevel": quantity,
                "minStockLevel": minStockLevel,
                "reOrderNeed": quantity <= minStockLevel,
            }
        )
        await prisma.models.InventoryEvent.prisma().create(
            data={
                "itemId": item.id,
                "eventType": prisma.enums.InventoryEventType.RECEIVED,
                "quantityChange": quantity,
                "date": acquisitionDate,
            }
        )
        return CreateInventoryItemResponse(
            success=True, message="Inventory item successfully added.", itemId=item.id
        )
    except Exception as e:
        return CreateInventoryItemResponse(
            success=False, message=f"Failed to add item: {str(e)}", itemId=0
        )
