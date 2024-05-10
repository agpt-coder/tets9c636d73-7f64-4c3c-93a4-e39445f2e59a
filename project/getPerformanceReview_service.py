from datetime import datetime
from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class PerformanceReviewResponse(BaseModel):
    """
    Response model containing the details of the fetched performance review. Roles like HR Manager and System Administrator are expected to use this for making decisions or providing feedback.
    """

    id: int
    user_id: int
    review_date: datetime
    score: int
    feedback: Optional[str] = None


async def getPerformanceReview(id: int) -> PerformanceReviewResponse:
    """
    Fetches a specific performance review by its unique ID. This is useful for HR managers and system administrators when looking into the details of a particular employee's performance evaluation.

    Args:
        id (int): Unique identifier for the performance review to be fetched.

    Returns:
        PerformanceReviewResponse: Response model containing the details of the fetched performance review. Roles like HR Manager and System Administrator are expected to use this for making decisions or providing feedback.

    Example:
        # Example usage to retrieve performance review details:
        performance_review = getPerformanceReview(1)
    """
    review = await prisma.models.PerformanceReview.prisma().find_unique(
        where={"id": id}
    )
    if not review:
        raise ValueError(f"No performance review found with ID {id}")
    return PerformanceReviewResponse(
        id=review.id,
        user_id=review.userId,
        review_date=review.reviewDate,
        score=review.score,
        feedback=review.feedback,
    )
