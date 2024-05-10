from datetime import datetime, time
from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class ScheduleTreeTreatmentResponse(BaseModel):
    """
    Confirms the details of the treatment scheduling along with any necessary metadata for tracking.
    """

    success: bool
    scheduled_id: int
    message: str


async def scheduleTreatment(
    tree_ids: List[int],
    treatment_type: str,
    scheduled_date: datetime,
    scheduled_time: time,
) -> ScheduleTreeTreatmentResponse:
    """
    Schedules a new treatment for one or more trees. Inputs would include tree IDs, treatment type, scheduled date and time. It ensures all treatments are timely and recorded for future reference.

    Args:
        tree_ids (List[int]): A list of tree IDs for which the treatment is to be scheduled.
        treatment_type (str): Type of treatment to be applied to the trees.
        scheduled_date (datetime): The scheduled date for the treatment.
        scheduled_time (time): The specific time at which the treatment should occur on the scheduled date.

    Returns:
        ScheduleTreeTreatmentResponse: Confirms the details of the treatment scheduling along with any necessary metadata for tracking.

    Example:
        tree_ids = [1, 2, 3]
        treatment_type = 'Fertilization'
        schedule_date = datetime(2023, 12, 25)
        schedule_time = time(10, 0)
        response = await scheduleTreatment(tree_ids, treatment_type, schedule_date, schedule_time)
        # This example assumes treatment scheduling was successful.
        print(response)
    """
    try:
        combined_datetime = datetime.combine(scheduled_date, scheduled_time)
        schedule = await prisma.models.Schedule.prisma().create(
            {"scheduledOn": combined_datetime, "type": "TREATMENT", "status": "PENDING"}
        )
        treatment_details = f"Scheduled {treatment_type} for trees with IDs {tree_ids} at {combined_datetime}"
        return ScheduleTreeTreatmentResponse(
            success=True, scheduled_id=schedule.id, message=treatment_details
        )
    except Exception as e:
        return ScheduleTreeTreatmentResponse(
            success=False, scheduled_id=0, message=str(e)
        )
