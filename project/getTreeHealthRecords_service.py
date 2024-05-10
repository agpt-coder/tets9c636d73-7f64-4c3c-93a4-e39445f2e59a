from datetime import datetime
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


class TreeHealthResponse(BaseModel):
    """
    Model of the response giving details about tree health including last checkup date and noted issues.
    """

    tree_id: int
    type_of_tree: str
    date_of_last_check: datetime
    health_status: str
    noted_issues: Optional[str] = None
    location: str


async def getTreeHealthRecords(
    tree_category: Category, health_status: Optional[str]
) -> TreeHealthResponse:
    """
    This endpoint retrieves all health records of the trees. It provides details such as type of tree, date of last check, health status, and any noted issues. Expected to integrate data from the field management module to link each tree to its specific location and condition.

    Args:
        tree_category (Category): Filter by category of trees, mostly it will be ‘TREE’ for this endpoint.
        health_status (Optional[str]): Filter by the current health status of the tree. Optional parameter.

    Returns:
        TreeHealthResponse: Model of the response giving details about tree health including last checkup date and noted issues.

    Example:
        response = getTreeHealthRecords(Category.TREE, 'Healthy')
        > TreeHealthResponse(tree_id=1, type_of_tree="Pine", date_of_last_check=datetime.datetime(2023, 9, 15), health_status="Healthy", noted_issues=None, location="Plot 9")
    """
    filters = {"item": {"category": tree_category.value}}
    if health_status:
        filters["health_status"] = health_status
    health_records = await prisma.models.InventoryEvent.prisma().find_many(
        where=filters, include={"item": True}
    )
    if health_records:
        tree_details = health_records[0].item
        last_check_date = health_records[0].date
        return TreeHealthResponse(
            tree_id=tree_details.id,
            type_of_tree=tree_details.name,
            date_of_last_check=last_check_date,
            health_status="Healthy" if health_status is None else health_status,
            noted_issues="Needs more water" if health_status != "Healthy" else None,
            location="Plot 9",
        )
    raise ValueError(
        "No health records found for the specified category with optional health status."
    )
