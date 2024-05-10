from datetime import datetime
from enum import Enum

import prisma
import prisma.models
from pydantic import BaseModel


class Category(Enum):
    """
    Enum representing different categories of items in inventory
    """

    value: str  # TODO(autogpt): "value" incorrectly overrides property of same name in class "Enum". reportIncompatibleMethodOverride


class SupplyChainReportResponse(BaseModel):
    """
    This model encapsulates the supply chain report data including key performance indicators, scheduling details, and cost analyses tied to the supply chain operations.
    """

    report_overview: str
    supplier_performance: str
    delivery_metrics: str
    cost_analysis: str


async def fetchSupplyChainReports(
    start_date: datetime, end_date: datetime, item_category: Category
) -> SupplyChainReportResponse:
    """
    Retrieves reports specific to supply chain operations, sourced from the Supply Chain Module. This includes supplier performance, delivery schedules, and cost analyses, important for optimizing the overall supply chain efficiency.

    Args:
        start_date (datetime): The starting date from which to begin fetching the report data.
        end_date (datetime): The end date until which the report data should be fetched.
        item_category (Category): Filter reports by the category of items included in the supply chain (e.g., FERTILIZER, TREE).

    Returns:
        SupplyChainReportResponse: This model encapsulates the supply chain report data including key performance indicators, scheduling details, and cost analyses tied to the supply chain operations.
    """
    events = await prisma.models.InventoryEvent.prisma().find_many(
        where={
            "date": {"gte": start_date, "lte": end_date},
            "item": {"category": item_category.name},
        },
        include={"item": True},
    )
    report_overview = f"Supply chain report for {item_category.name} from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}."
    supplier_performance = f"Analyzing performance for {len(events)} events."
    delivery_metrics = f"Averaged {(sum((e.quantityChange for e in events if e.eventType == 'RECEIVED')) / len(events) if events else 0):.2f} units received per event."
    cost_analysis = "Total costs and savings to be calculated based on real data and business logic."
    return SupplyChainReportResponse(
        report_overview=report_overview,
        supplier_performance=supplier_performance,
        delivery_metrics=delivery_metrics,
        cost_analysis=cost_analysis,
    )
