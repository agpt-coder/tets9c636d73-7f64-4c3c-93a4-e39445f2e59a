from datetime import datetime
from typing import List, Optional

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class FetchStaffSchedulesRequest(BaseModel):
    """
    This model does not require any fields, as the request fetches all staff schedules irrespective of specific input parameters. Authorization headers or tokens should be used to ensure only privileged sessions can access this data.
    """

    pass


class UserProfileMinimal(BaseModel):
    """
    Minimal essential details of a user relevant to the schedule context.
    """

    user_id: int
    first_name: str
    last_name: str
    contact_number: Optional[str] = None


class ScheduleDetailed(BaseModel):
    """
    Expanded details for a schedule, including user and status details.
    """

    scheduled_on: datetime
    type: prisma.enums.ScheduleType
    status: prisma.enums.ScheduleStatus
    user_details: UserProfileMinimal


class FetchStaffSchedulesResponse(BaseModel):
    """
    Contains a list of all staff schedules, detailed with user association, status, and type. This model will deliver a comprehensive overview, suitable for managerial oversight and planning.
    """

    schedules: List[ScheduleDetailed]


async def getSchedule(
    request: FetchStaffSchedulesRequest,
) -> FetchStaffSchedulesResponse:
    """
    Fetches all staff schedules. This route retrieves complete schedule details from the database. It's intended for viewing the entire set of schedules by authorized managers.

    Args:
        request (FetchStaffSchedulesRequest): This model does not require any fields, as the request fetches all staff schedules irrespective of specific input parameters. Authorization headers or tokens should be used to ensure only privileged sessions can access this data.

    Returns:
        FetchStaffSchedulesResponse: Contains a list of all staff schedules, detailed with user association, status, and type. This model will deliver a comprehensive overview, suitable for managerial oversight and planning.
    """
    all_schedules = await prisma.models.Schedule.prisma().find_many(
        include={"user": {"include": {"profile": True}}}
    )
    detailed_schedules = []
    for schedule in all_schedules:
        if schedule.user and schedule.user.profile:
            user_details = UserProfileMinimal(
                user_id=schedule.user.id,
                first_name=schedule.user.profile.firstName,
                last_name=schedule.user.profile.lastName,
                contact_number=schedule.user.profile.contactNumber,
            )
        else:
            user_details = UserProfileMinimal(
                user_id=0,
                first_name="Unknown",
                last_name="Unknown",
                contact_number=None,
            )
        detailed_schedule = ScheduleDetailed(
            scheduled_on=schedule.scheduledOn,
            type=schedule.type,
            status=schedule.status,
            user_details=user_details,
        )
        detailed_schedules.append(detailed_schedule)
    return FetchStaffSchedulesResponse(schedules=detailed_schedules)
