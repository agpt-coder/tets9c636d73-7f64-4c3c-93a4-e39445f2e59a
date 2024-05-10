from datetime import datetime
from typing import Optional

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class Role(BaseModel):
    """
    Enum representing various system roles.
    """

    role_value: str


class UserProfile(BaseModel):
    """
    Supplementary profile model for users containing non-authentication specific details.
    """

    lastName: str
    firstName: str
    contactNumber: Optional[str] = None


class User(BaseModel):
    """
    Model representing a user, including their roles and profile details.
    """

    id: int
    email: str
    role: Role
    profile: Optional[UserProfile] = None


class ScheduleResponse(BaseModel):
    """
    This response model encapsulates the details of a schedule, providing comprehensive data crucial for managing scheduling tasks.
    """

    id: int
    scheduledOn: datetime
    type: prisma.enums.ScheduleType
    user: Optional[User] = None
    status: prisma.enums.ScheduleStatus


async def getScheduleById(id: int) -> ScheduleResponse:
    """
    Fetches a specific schedule entry by ID. This endpoint is crucial for retrieving detailed information
    about a particular schedule, including tasks, assigned resources, and timings. The response will provide
    comprehensive details needed for precise management of activities.

    Args:
        id (int): The unique identifier of the schedule to be fetched.

    Returns:
        ScheduleResponse: This response model encapsulates the details of a schedule,
                          providing comprehensive data crucial for managing scheduling tasks.
    """
    schedule = await prisma.models.Schedule.prisma().find_unique(
        where={"id": id}, include={"user": {"include": {"profile": True}}}
    )
    if not schedule:
        raise Exception("Schedule not found")
    schedule_user = schedule.user
    user_profile = (
        schedule_user.profile if schedule_user and schedule_user.profile else None
    )
    user_data = (
        User(
            id=schedule_user.id,
            email=schedule_user.email,
            role=schedule_user.role,
            profile=user_profile,
        )
        if schedule_user
        else None
    )
    return ScheduleResponse(
        id=schedule.id,
        scheduledOn=schedule.scheduledOn,
        type=schedule.type,
        user=user_data,
        status=schedule.status,
    )
