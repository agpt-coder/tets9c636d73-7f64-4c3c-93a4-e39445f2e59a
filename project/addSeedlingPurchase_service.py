from datetime import datetime

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class SeedlingPurchaseResponse(BaseModel):
    """
    Confirms the recording and processing of a new seedling purchase and any associated inventory updates.
    """

    success: bool
    message: str


async def addSeedlingPurchase(
    supplier: str, quantity: int, cost: float, purchaseDate: str
) -> SeedlingPurchaseResponse:
    """
    Adds a new seedling purchase to the system. It records details of the purchase such as quantity, supplier, and cost.
    This action subsequently updates the Inventory through an internal API call that increases inventory levels.

    Args:
    supplier (str): The name or ID of the supplier from whom the seedlings are purchased.
    quantity (int): The number of seedlings purchased in this transaction.
    cost (float): The total cost of the seedling purchase.
    purchaseDate (str): The date the seedlings were purchased, formatted as YYYY-MM-DD.

    Returns:
    SeedlingPurchaseResponse: Confirms the recording and processing of a new seedling purchase and any associated inventory updates.
    """
    seedling_item = await prisma.models.Item.prisma().find_first(
        where={"name": "Seedling", "category": prisma.enums.Category.SAPLING}
    )
    if not seedling_item:
        return SeedlingPurchaseResponse(
            success=False, message="Seedling item not found in inventory."
        )
    try:
        event = await prisma.models.InventoryEvent.prisma().create(
            data={
                "item": {"connect": {"id": seedling_item.id}},
                "eventType": prisma.enums.InventoryEventType.RECEIVED,
                "quantityChange": quantity,
                "date": datetime.strptime(purchaseDate, "%Y-%m-%d"),
            }
        )
        await prisma.models.Item.prisma().update(
            where={"id": seedling_item.id},
            data={"stockLevel": seedling_item.stockLevel + quantity},
        )
        response_text = f"Successfully recorded purchase and updated inventory: +{quantity} seedlings."
        return SeedlingPurchaseResponse(success=True, message=response_text)
    except Exception as e:
        return SeedlingPurchaseResponse(
            success=False,
            message=f"Failed to record purchase or update inventory. Error: {str(e)}",
        )
