from enum import Enum
from typing import List

import prisma
import prisma.enums
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


async def getInventoryReport(
    request: InventoryReportRequest,
) -> InventoryReportResponse:
    """
    Generates a detailed report on inventory status which helps in decision-making. It interacts with the Reporting Module for real-time data and displays items grouped by type, status, and impending stock-outs.

    Args:
        request (InventoryReportRequest): This model is used to fetch data required to generate a detailed inventory report. The request itself doesn't require any specific inputs as it retrieves data based on current inventory states and events.

    Returns:
        InventoryReportResponse: This response model provides detailed inventory status categorized by item type, stock status, and alerts for any impending stock-outs.
    """
    items = await prisma.models.Item.prisma().find_many(
        include={"inventoryEvents": True}
    )
    report_details = []
    for item in items:
        pending_transactions = sum(
            (
                event.quantityChange
                for event in item.inventoryEvents or []
                if event.eventType == prisma.enums.InventoryEventType.RECEIVED
            )
        )
        if item.stockLevel >= item.minStockLevel:
            stock_status = "Sufficient"
        elif item.stockLevel > 0 and item.stockLevel < item.minStockLevel:
            stock_status = "Low"
        else:
            stock_status = "Critical"
        report_details.append(
            InventoryReportDetail(
                itemCategory=item.category,
                itemName=item.name,
                currentStock=item.stockLevel,
                minStockLevel=item.minStockLevel,
                stockStatus=stock_status,
                pendingTransactions=pending_transactions,
            )
        )
    return InventoryReportResponse(reports=report_details)
