import prisma
import prisma.models
from pydantic import BaseModel


class DeleteScheduleResponseModel(BaseModel):
    """
    Confirms the deletion of the schedule entry. Contains a message about the result of the request.
    """

    message: str


async def deleteSchedule(id: int) -> DeleteScheduleResponseModel:
    """
    Deletes a schedule entry. This endpoint facilitates the removal of outdated or completed schedules, ensuring that the system remains updated with only the relevant schedules. It helps in maintaining clarity and focus on current and future tasks.

    Args:
    id (int): Unique identifier for the schedule to be deleted.

    Returns:
    DeleteScheduleResponseModel: Confirms the deletion of the schedule entry. Contains a message about the result of the request.

    Raises:
        Exception: If no schedule is found with the given ID or if the delete operation fails.
    """
    schedule = await prisma.models.Schedule.prisma().find_unique(where={"id": id})
    if not schedule:
        raise Exception("prisma.models.Schedule with the given ID does not exist")
    delete_result = await prisma.models.Schedule.prisma().delete(where={"id": id})
    if delete_result:
        return DeleteScheduleResponseModel(
            message="prisma.models.Schedule deleted successfully."
        )
    else:
        raise Exception("Failed to delete the schedule")
