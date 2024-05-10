import prisma
import prisma.models
from pydantic import BaseModel


class DeleteTreeHealthRecordResponse(BaseModel):
    """
    Response model indicating the success or failure of a tree health record deletion.
    """

    success: bool
    message: str


async def deleteTreeHealthRecord(id: str) -> DeleteTreeHealthRecordResponse:
    """
    Deletes a tree health record when it is no longer needed or if entered in error. The operation requires the
    tree health record ID and is restricted to maintain data integrity.

    Args:
        id (str): The unique identifier of the tree health record to be deleted.

    Returns:
        DeleteTreeHealthRecordResponse: Response model indicating the success or failure of a tree health record deletion.
    """
    record = await prisma.models.Item.prisma().find_unique(where={"id": int(id)})
    if not record:
        return DeleteTreeHealthRecordResponse(
            success=False, message="Tree health record not found."
        )
    await prisma.models.Item.prisma().delete(where={"id": int(id)})
    return DeleteTreeHealthRecordResponse(
        success=True, message="Tree health record successfully deleted."
    )
