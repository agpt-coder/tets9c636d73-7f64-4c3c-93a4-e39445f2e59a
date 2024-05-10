from datetime import datetime
from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class CreatePerformanceReviewResponse(BaseModel):
    """
    Confirmation of the creation of a new performance review. Includes the details of the review that was added.
    """

    success: bool
    reviewId: int
    message: str


async def createPerformanceReview(
    userId: int, reviewDate: datetime, score: int, feedback: Optional[str]
) -> CreatePerformanceReviewResponse:
    """
    Creates a new performance review. The API will accept data such as employee ID, review metrics, and optional notes. This endpoint is crucial for documenting and initiating new evaluations.

    Args:
        userId (int): The unique identifier of the employee for whom the performance review is being conducted.
        reviewDate (datetime): The date on which the performance review is conducted. If not provided, it defaults to the current date.
        score (int): Numerical metric (score) reflecting performance, typically on a scale (e.g., 1-100).
        feedback (Optional[str]): Optional textual feedback providing more insights into the performance.

    Returns:
        CreatePerformanceReviewResponse: Confirmation of the creation of a new performance review. Includes the details of the review that was added.
    """
    user = await prisma.models.User.prisma().find_unique(where={"id": userId})
    if user is None:
        return CreatePerformanceReviewResponse(
            success=False, reviewId=-1, message=f"No user found with ID {userId}"
        )
    created_review = await prisma.models.PerformanceReview.prisma().create(
        data={
            "userId": userId,
            "reviewDate": reviewDate,
            "score": score,
            "feedback": feedback,
        }
    )
    return CreatePerformanceReviewResponse(
        success=True,
        reviewId=created_review.id,
        message="Successfully created the performance review",
    )
