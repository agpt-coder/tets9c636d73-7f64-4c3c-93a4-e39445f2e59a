from enum import Enum
from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class Category(Enum):
    """
    Enum representing different categories of items in inventory
    """

    value: str  # TODO(autogpt): "value" incorrectly overrides property of same name in class "Enum". reportIncompatibleMethodOverride


class SaplingDetails(BaseModel):
    """
    Detailed description of each sapling item, including its stock level and order necessity.
    """

    item_id: int
    name: str
    stockLevel: int
    reOrderNeed: bool


class FetchSeedlingsResponse(BaseModel):
    """
    Provides a listing of seedlings available for purchase based on the reOrderNeed flag and categorization. Each seedling has key details included to assist in purchasing decisions.
    """

    seedlings: List[SaplingDetails]


async def listSeedlings(category: Category) -> FetchSeedlingsResponse:
    """
    Retrieves a list of all seedlings available for purchase. This function filters seedlings based on the category and combined with the reOrderNeed flag.

    Args:
        category (Category): Specifies the category of items to fetch seedlings.

    Returns:
        FetchSeedlingsResponse: Provides a listing of seedlings available for purchase based on the reOrderNeed flag and categorization. Each seedling has key details included to assist in purchasing decisions.
    """
    items = await prisma.models.Item.prisma().find_many(
        where={"category": category.name, "reOrderNeed": True}
    )
    seedlings = [
        SaplingDetails(
            item_id=item.id,
            name=item.name,
            stockLevel=item.stockLevel,
            reOrderNeed=item.reOrderNeed,
        )
        for item in items
    ]
    return FetchSeedlingsResponse(seedlings=seedlings)
