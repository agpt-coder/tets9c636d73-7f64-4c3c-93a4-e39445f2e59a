from datetime import datetime
from typing import List

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class ScheduleDetails(BaseModel):
    """
    Details of a schedule that has been affected by the field assignment update.
    """

    scheduleId: int
    newScheduledDate: datetime
    status: prisma.enums.ScheduleStatus


class SchedulesByRoleResponse(BaseModel):
    """
    Provides a detailed list of schedules associated with a specific staff role, including relevant user and status details.
    """

    schedules: List[ScheduleDetails]


async def getScheduleByRole(roleId: str) -> SchedulesByRoleResponse:
    """
    Retrieves schedules based on staff role. This function utilizes a lookup to the Staff Roles Management Module to fetch schedules specific to a particular role, crucial for role-based planning and coverage efficiency.

    Args:
        roleId (str): The unique identifier of the staff role for which schedules are to be fetched.

    Returns:
        SchedulesByRoleResponse: Provides a detailed list of schedules associated with a specific staff role, including relevant user and status details.

    Example:
        getScheduleByRole("FIELD_MANAGER")
        > SchedulesByRoleResponse(schedules=[
            ScheduleDetails(scheduleId=1, newScheduledDate=datetime(2023, 12, 25), status="COMPLETED"),
            ScheduleDetails(scheduleId=2, newScheduledDate=datetime(2023, 12, 26), status="PENDING")
          ])
    """
    schedules = await prisma.models.Schedule.prisma().find_many(
        where={"user": {"role": roleId}}, include={"user": True}
    )
    result_schedules = [
        ScheduleDetails(
            scheduleId=schedule.id,
            newScheduledDate=schedule.scheduledOn,
            status=schedule.status,
        )
        for schedule in schedules
    ]
    return SchedulesByRoleResponse(schedules=result_schedules)
