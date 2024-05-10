from datetime import datetime

import prisma
import prisma.models
from pydantic import BaseModel


class TreeHealthRecord(BaseModel):
    """
    Detailed Pydantic model of a tree health record, capturing all necessary details.
    """

    tree_id: int
    health_status: str
    issues_detected: str
    date_of_assessment: datetime


class TreeHealthPostResponse(BaseModel):
    """
    Provides a confirmation of the health record creation with details of the recorded entry.
    """

    success: bool
    message: str
    tree_health_record: TreeHealthRecord


async def addTreeHealthRecord(
    tree_id: int, health_status: str, issues_detected: str, date_of_assessment: datetime
) -> TreeHealthPostResponse:
    """
    Allows the creation of a new health record for a tree. Fields to input include tree ID, health status,
    issues detected, and the date of assessment. This is crucial for recording periodic health checks and treatments.

    Args:
        tree_id (int): The unique identifier of the tree for which the health record is being created.
        health_status (str): The current health status of the tree.
        issues_detected (str): A brief description of any issues detected during the health assessment of the tree.
        date_of_assessment (datetime): The date on which the health assessment was carried out.

    Returns:
        TreeHealthPostResponse: Provides a confirmation of the health record creation with details of the recorded entry.

    Example:
        > addTreeHealthRecord(
              tree_id=1,
              health_status='Healthy',
              issues_detected='No issues',
              date_of_assessment=datetime(2023,12,25)
          )
        > TreeHealthPostResponse(success=True, message="Health record created.", ...)
    """
    tree_check = await prisma.models.Item.prisma().find_first(
        where={"id": tree_id, "category": "TREE"}
    )
    if not tree_check:
        return TreeHealthPostResponse(
            success=False,
            message="Invalid tree ID or tree does not exist.",
            tree_health_record=None,
        )
    new_record = TreeHealthRecord(
        tree_id=tree_id,
        health_status=health_status,
        issues_detected=issues_detected,
        date_of_assessment=date_of_assessment,
    )
    return TreeHealthPostResponse(
        success=True,
        message="Health record successfully created.",
        tree_health_record=new_record,
    )
