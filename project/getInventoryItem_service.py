from datetime import datetime
from enum import Enum
from typing import List

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class Category(Enum):
    """
    Enum representing different categories of items in inventory
    """

    value: str  # TODO(autogpt): "value" incorrectly overrides property of same name in class "Enum". reportIncompatibleMethodOverride


class InventoryEventDetail(BaseModel):
    """
    Detailed record of an inventory-related event, such as receiving or shipping stock.
    """

    eventType: prisma.enums.InventoryEventType
    quantityChange: int
    date: datetime


class InventoryItemDetailsResponse(BaseModel):
    """
    Provides a detailed view of an inventory item, including current stock levels, sourcing details, and a history of inventory events.
    """

    id: int
    name: str
    category: Category
    stockLevel: int
    minStockLevel: int
    reOrderNeed: bool
    inventoryEvents: List[InventoryEventDetail]


async def getInventoryItem(itemId: int) -> InventoryItemDetailsResponse:
    """
    Retrieves detailed information for a specific inventory item by ID, including stock levels, sourcing information,
    and item history. Useful for audits and detailed reports.

    Args:
        itemId (int): The unique identifier for the inventory item whose details are being requested.

    Returns:
        InventoryItemDetailsResponse: Provides a detailed view of an inventory item, including current stock levels,
        sourcing details, and a history of inventory events.

    Example:
        # Assume you have an inventory item with ID 1
        details = await getInventoryItem(1)
        print(details)
    """
    item = await prisma.models.Item.prisma().find_unique(
        where={"id": itemId}, include={"inventoryEvents": True}
    )
    if item is None:
        raise ValueError(f"Inventory item with ID {itemId} not found.")
    inventory_events_details = (
        [
            {
                "eventType": event.eventType.value,
                "quantityChange": event.quantityChange,
                "date": event.date.isoformat(),
            }
            for event in item.inventoryEvents
        ]
        if item.inventoryEvents
        else []
    )
    item_details = InventoryItemDetailsResponse(
        id=item.id,
        name=item.name,
        category=item.category.value,
        stockLevel=item.stockLevel,
        minStockLevel=item.minStockLevel,
        reOrderNeed=item.reOrderNeed,
        inventoryEvents=inventory_events_details,
    )
    return item_details
