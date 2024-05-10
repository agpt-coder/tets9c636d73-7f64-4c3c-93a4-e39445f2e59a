from datetime import datetime
from typing import List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class GetPerformanceReviewsRequest(BaseModel):
    """
    Request model for getting all performance reviews. No parameters needed for this unfiltered retrieval.
    """

    pass


class PerformanceReview(BaseModel):
    """
    Performance review data model holding all details related to employee evaluations.
    """

    id: int
    userId: int
    reviewDate: datetime
    score: int
    feedback: Optional[str] = None


class GetPerformanceReviewsResponse(BaseModel):
    """
    Contains the list of all performance reviews including detailed information for HR oversight purposes. Maps directly onto the PerformanceReview database model.
    """

    reviews: List[PerformanceReview]


async def getPerformanceReviews(
    request: GetPerformanceReviewsRequest,
) -> GetPerformanceReviewsResponse:
    """
    Retrieves all performance reviews from the database. Each review contains details such as employee ID, review date, performance scores, and attached notes. Useful for HR managers to oversee staff evaluations.

    Args:
        request (GetPerformanceReviewsRequest): Request model for getting all performance reviews. No parameters needed for this unfiltered retrieval.

    Returns:
        GetPerformanceReviewsResponse: Contains the list of all performance reviews including detailed information for HR oversight purposes. Maps directly onto the PerformanceReview database model.
    """
    reviews = await prisma.models.PerformanceReview.prisma().find_many(
        include={"user": True}
    )
    mapped_reviews = [
        PerformanceReview(
            id=review.id,
            userId=review.userId,
            reviewDate=review.reviewDate,
            score=review.score,
            feedback=review.feedback,
        )
        for review in reviews
    ]
    return GetPerformanceReviewsResponse(reviews=mapped_reviews)
