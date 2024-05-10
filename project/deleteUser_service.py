import prisma
import prisma.models
from pydantic import BaseModel


class DeleteUserResponse(BaseModel):
    """
    Response model representing the outcome of a user deletion operation, confirming the successful deletion of the user.
    """

    confirmation: str


async def deleteUser(userId: int) -> DeleteUserResponse:
    """
    Deletes a user's profile from the system based on the given user ID. A successful operation returns a confirmation of deletion. Mainly managed by system administrators to maintain the integrity of user access.

    Args:
    userId (int): The unique identifier of the user to delete.

    Returns:
    DeleteUserResponse: Response model representing the outcome of a user deletion operation, confirming the successful deletion of the user.

    Example:
        deleted_user = await deleteUser(10)
        print(deleted_user.confirmation)
        > 'User with ID 10 has been successfully deleted.'
    """
    user = await prisma.models.User.prisma().delete(where={"id": userId})
    if user:
        return DeleteUserResponse(
            confirmation=f"User with ID {userId} has been successfully deleted."
        )
    else:
        return DeleteUserResponse(confirmation="User not found or deletion failed.")
