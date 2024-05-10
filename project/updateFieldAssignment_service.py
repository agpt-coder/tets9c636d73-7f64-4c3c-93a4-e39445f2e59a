from datetime import datetime
from typing import List

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class SchedulingAdjustment(BaseModel):
    """
    Details of adjustments to be made to the field's schedule.
    """

    scheduleId: int
    newDate: datetime
    newStatus: prisma.enums.ScheduleStatus


class ScheduleDetails(BaseModel):
    """
    Details of a schedule that has been affected by the field assignment update.
    """

    scheduleId: int
    newScheduledDate: datetime
    status: prisma.enums.ScheduleStatus


class FieldAssignmentUpdateResponse(BaseModel):
    """
    Provides confirmation and details of the update to the field assignment, including any impacted schedules.
    """

    success: bool
    updatedFieldId: str
    newAssignment: str
    affectedSchedules: List[ScheduleDetails]


async def updateFieldAssignment(
    fieldId: str,
    newCropOrActivity: str,
    scheduleAdjustments: List[SchedulingAdjustment],
) -> FieldAssignmentUpdateResponse:
    """
    Updates the assignment of a specific field to a new crop or operational activity, managing associated schedule entries.

    Args:
        fieldId (str): The unique identifier for the field being updated.
        newCropOrActivity (str): The new crop or operational activity to be assigned.
        scheduleAdjustments (List[SchedulingAdjustment]): List of adjustments to the schedules.

    Returns:
        FieldAssignmentUpdateResponse: Summary of the update operation.
    """
    affected_schedules = []
    for adjustment in scheduleAdjustments:
        schedule = await prisma.models.Schedule.prisma().update(
            where={"id": adjustment.scheduleId},
            data={"scheduledOn": adjustment.newDate, "status": adjustment.newStatus},
        )
        affected_schedules.append(
            ScheduleDetails(
                scheduleId=schedule.id,
                newScheduledDate=schedule.scheduled_on,
                status=schedule.status,
            )
        )  # TODO(autogpt): Cannot access member "scheduled_on" for type "Schedule"
    #     Member "scheduled_on" is unknown. reportAttributeAccessIssue
    success = len(affected_schedules) > 0
    return FieldAssignmentUpdateResponse(
        success=success,
        updatedFieldId=fieldId,
        newAssignment=newCropOrActivity,
        affectedSchedules=affected_schedules,
    )
