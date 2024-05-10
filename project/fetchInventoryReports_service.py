from enum import Enum
from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class InventoryReportRequest(BaseModel):
    """
    This model is used to fetch data required to generate a detailed inventory report. The request itself doesn't require any specific inputs as it retrieves data based on current inventory states and events.
    """

    pass


class Category(Enum):
    """
    Enum representing different categories of items in inventory
    """

    value: str  # TODO(autogpt): "value" incorrectly overrides property of same name in class "Enum". reportIncompatibleMethodOverride


class InventoryReportDetail(BaseModel):
    """
    Detail of the inventory report showing the item, current stock, pending transactions and stock status.
    """

    itemCategory: Category
    itemName: str
    currentStock: int
    minStockLevel: int
    stockStatus: str
    pendingTransactions: int


class InventoryReportResponse(BaseModel):
    """
    This response model provides detailed inventory status categorized by item type, stock status, and alerts for any impending stock-outs.
    """

    reports: List[InventoryReportDetail]


async def fetchInventoryReports(
    request: InventoryReportRequest,
) -> InventoryReportResponse:
    """
    Provides comprehensive inventory reports, combining information from Inventory Management.
    The expected response includes current stock levels, pending orders, and item usage statistics.
    Data is sourced from the Inventory Module to maintain updated and consistent inventory tracking.

    Args:
        request (InventoryReportRequest): Model used to fetch data required to generate a detailed inventory report.

    Returns:
        InventoryReportResponse: This response model provides detailed inventory status categorized by item type,
                                 stock status, and alerts for any impending stock-outs.
    """
    items = await prisma.models.Item.prisma().find_many(
        include={"inventoryEvents": True}
    )
    details = []
    for item in items:
        pending_transactions = sum(
            (
                event.quantityChange
                for event in item.inventoryEvents
                if event.eventType != "SHIPPED"
            )
        )
        stock_status = "Sufficient"
        if item.stockLevel <= item.minStockLevel / 2:
            stock_status = "Critical"
        elif item.stockLevel < item.minStockLevel:
            stock_status = "Low"
        detail = InventoryReportDetail(
            itemCategory=item.category,
            itemName=item.name,
            currentStock=item.stockLevel,
            minStockLevel=item.minStockLevel,
            stockStatus=stock_status,
            pendingTransactions=pending_transactions,
        )
        details.append(detail)
    return InventoryReportResponse(reports=details)
