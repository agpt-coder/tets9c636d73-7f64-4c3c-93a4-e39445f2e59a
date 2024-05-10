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


async def updatePerformanceReview(
    id: int, score: int, feedback: Optional[str]
) -> PerformanceReviewResponse:
    """
    Updates an existing performance review. This can include changes to scores, notes, or review outcomes. This endpoint ensures performance records are current and reflect any new developments or reassessments.

    Args:
        id (int): The identifier of the specific performance review being updated.
        score (int): The new score to be set for the performance review. Scores typically could be scaled from 1 to 10.
        feedback (Optional[str]): Optional feedback text providing additional insights or comments on the staff member's performance.

    Returns:
        PerformanceReviewResponse: Response model containing the details of the updated performance review.
    """
    review = await prisma.models.PerformanceReview.prisma().find_unique(
        where={"id": id}
    )
    if not review:
        raise ValueError(f"No performance review found with ID {id}")
    updated_review = await prisma.models.PerformanceReview.prisma().update(
        where={"id": id}, data={"score": score, "feedback": feedback or review.feedback}
    )
    return PerformanceReviewResponse(
        id=updated_review.id,
        user_id=updated_review.user_id,
        review_date=updated_review.review_date,
        score=updated_review.score,
        feedback=updated_review.feedback,
    )  # TODO(autogpt): Cannot access member "user_id" for type "PerformanceReview"


#     Member "user_id" is unknown. reportAttributeAccessIssue
