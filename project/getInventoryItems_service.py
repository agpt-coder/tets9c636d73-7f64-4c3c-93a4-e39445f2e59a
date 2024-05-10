from enum import Enum
from typing import List, Optional

import prisma
import prisma.models
from models import Category, GetInventoryItemsResponse, Item
from pydantic import BaseModel


class Category(Enum):
    """
    Enum representing different categories of items in inventory
    """

    value: str  # TODO(autogpt): "value" incorrectly overrides property of same name in class "Enum". reportIncompatibleMethodOverride


class Item(BaseModel):
    """
    Details about each item within the order.
    """

    name: str
    quantity: int
    pricePerItem: float


class GetInventoryItemsResponse(BaseModel):
    """
    Outputs a list of items from the inventory based on the applied filters and pagination. Also provides general metadata about the pagination results.
    """

    items: List[Item]
    total_items: int
    total_pages: int
    current_page: int
    items_per_page: int


async def getInventoryItems(
    page: int,
    limit: int,
    filter_category: Optional[Category],
    filter_stock_level: Optional[int],
    sort_by: Optional[str],
) -> GetInventoryItemsResponse:
    """
    Retrieves a list of all inventory items including fertilizers, trees, and equipment. Each item includes details
    like stock levels, location, and type. This endpoint includes pagination and filtering options to handle large
    datasets effectively.

    Args:
        page (int): The page number in the pagination system.
        limit (int): The number of records to return per page.
        filter_category (Optional[Category]): Filter results based on item category such as FERTILIZER, TREE, EQUIPMENT, etc.
        filter_stock_level (Optional[int]): Filter results based on the minimum stock level required.
        sort_by (Optional[str]): Parameter to sort the results based on fields like 'name', 'stockLevel'.

    Returns:
        GetInventoryItemsResponse: Outputs a list of items from the inventory based on the applied filters and pagination.
        Also provides general metadata about the pagination results.
    """
    query_parameters = {
        "skip": (page - 1) * limit,
        "take": limit,
        "where": {},
        "order_by": {},
    }
    if filter_category is not None:
        query_parameters["where"]["category"] = filter_category.value
    if filter_stock_level is not None:
        query_parameters["where"]["stockLevel"] = {"gte": filter_stock_level}
    if sort_by:
        sort_order = "asc" if not sort_by.startswith("-") else "desc"
        field_name = sort_by.lstrip("-")
        query_parameters["order_by"] = {field_name: sort_order}
    items = await prisma.models.Item.prisma().find_many(**query_parameters)
    total_items = await prisma.models.Item.prisma().count(
        where=query_parameters["where"]
    )
    model_items = [
        Item(name=item.name, quantity=item.stockLevel, pricePerItem=0.0)
        for item in items
    ]
    total_pages = total_items // limit + (total_items % limit > 0)
    return GetInventoryItemsResponse(
        items=model_items,
        total_items=total_items,
        total_pages=total_pages,
        current_page=page,
        items_per_page=limit,
    )
