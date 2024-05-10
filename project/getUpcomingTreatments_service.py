from datetime import datetime, timedelta
from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class GetUpcomingTreeTreatmentsRequest(BaseModel):
    """
    This model contains no parameters as it fetches upcoming treatments based on the current date and schedules configured in the system.
    """

    pass


class TreeDetail(BaseModel):
    """
    Specific identifier and health status of the tree.
    """

    treeId: int
    healthStatus: str
    location: str


class TreatmentDetail(BaseModel):
    """
    Details of each scheduled treatment for trees.
    """

    date: datetime
    treatmentType: str
    tree: TreeDetail


class UpcomingTreeTreatmentsResponse(BaseModel):
    """
    Outputs a list of upcoming tree treatments including dates, treatment types, and details about the target trees where applicable.
    """

    treatments: List[TreatmentDetail]


async def getUpcomingTreatments(
    request: GetUpcomingTreeTreatmentsRequest,
) -> UpcomingTreeTreatmentsResponse:
    """
    Fetches a list of upcoming treatments scheduled. It integrates with the Scheduling Module to pull in data about planned dates, types of treatment, and target trees. This helps in preparing for necessary resources and staff allocation.

    Args:
    request (GetUpcomingTreeTreatmentsRequest): This model contains no parameters as it fetches upcoming treatments based on the current date and schedules configured in the system.

    Returns:
    UpcomingTreeTreatmentsResponse: Outputs a list of upcoming tree treatments including dates, treatment types, and details about the target trees where applicable.
    """
    current_date = datetime.now()
    end_date = current_date + timedelta(days=30)
    schedules = await prisma.models.Schedule.prisma().find_many(
        where={
            "scheduledOn": {"gte": current_date, "lte": end_date},
            "type": "HEALTH_SPECIALIST",
        }
    )
    treatment_details = []
    for schedule in schedules:
        tree_detail = TreeDetail(
            treeId=schedule.id, healthStatus="Good", location="North field"
        )
        treatment_detail = TreatmentDetail(
            date=schedule.scheduledOn, treatmentType="Fertilization", tree=tree_detail
        )
        treatment_details.append(treatment_detail)
    return UpcomingTreeTreatmentsResponse(treatments=treatment_details)
