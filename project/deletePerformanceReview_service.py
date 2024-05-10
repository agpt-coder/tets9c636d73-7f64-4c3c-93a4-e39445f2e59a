import prisma
import prisma.models
from pydantic import BaseModel


class DeletePerformanceReviewResponse(BaseModel):
    """
    A confirmation response model after deleting a performance review.
    """

    confirmation: str
    deletedId: int


async def deletePerformanceReview(id: int) -> DeletePerformanceReviewResponse:
    """
    Deletes a performance review by ID. This is critical for maintaining data integrity and removing outdated or incorrect evaluations.

    Args:
        id (int): The unique identifier of the performance review to be deleted.

    Returns:
        DeletePerformanceReviewResponse: A confirmation response model after deleting a performance review.

    Example:
        deletePerformanceReview(101)
    """
    deleted_review = await prisma.models.PerformanceReview.prisma().delete(
        where={"id": id}
    )
    return DeletePerformanceReviewResponse(
        confirmation="Performance review successfully deleted.", deletedId=id
    )
