import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class DeleteFarmLayoutResponse(BaseModel):
    """
    Response model indicating the success or failure of the farm layout deletion.
    """

    status: str
    message: str


async def deleteFarmLayout(layoutId: str) -> DeleteFarmLayoutResponse:
    """
    Deletes a specified farm layout via ID. The system should ensure that the layout does not contain any active assignments
    or important linkages with other ongoing activities before deletion. Provides a means to clean up unused or outdated maps.

    Args:
        layoutId (str): The unique identifier of the farm layout to be deleted.

    Returns:
        DeleteFarmLayoutResponse: Response model indicating the success or failure of the farm layout deletion.

    Example:
        response = deleteFarmLayout("123")
        print(response.status)  # 'Success' or 'Failure'
        print(response.message)  # 'Layout deleted successfully.' or 'Layout cannot be deleted: <reason>'
    """
    active_schedules = await prisma.models.Schedule.prisma().find_many(
        where={
            "userId": layoutId,
            "status": {"not": prisma.enums.ScheduleStatus.COMPLETED},
        }
    )
    if active_schedules:
        return DeleteFarmLayoutResponse(
            status="Failure",
            message="Layout cannot be deleted as it's associated with active schedules.",
        )
    delete_result = await prisma.models.User.prisma().delete(where={"id": layoutId})
    if delete_result:
        return DeleteFarmLayoutResponse(
            status="Success", message="Layout deleted successfully."
        )
    else:
        return DeleteFarmLayoutResponse(
            status="Failure",
            message="Failed to delete layout. It may not exist or some error occurred.",
        )
