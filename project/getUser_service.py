from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class Role(BaseModel):
    """
    Enum representing various system roles.
    """

    role_value: str


class UserProfile(BaseModel):
    """
    Supplementary profile model for users containing non-authentication specific details.
    """

    lastName: str
    firstName: str
    contactNumber: Optional[str] = None


class GetUserProfileResponse(BaseModel):
    """
    Response model returning the detailed profile of a user, excluding their password and any other sensitive data.
    """

    id: int
    email: str
    role: Role
    profile: UserProfile


async def getUser(userId: int) -> GetUserProfileResponse:
    """
    Retrieves a specific user's profile using the userID passed as a path parameter. It provides detailed user data except
    for the password. Used mostly by system administrators or for the respective user to view their information.

    Args:
        userId (int): Unique identifier of the user whose profile is being retrieved.

    Returns:
        GetUserProfileResponse: Response model returning the detailed profile of a user, excluding their password and
        any other sensitive data.

    Example:
        user_profile = await getUser(1)
        print(user_profile)  # Output would be GetUserProfileResponse object showing user details.
    """
    user_data = await prisma.models.User.prisma().find_unique(
        where={"id": userId}, include={"profile": True}
    )
    if not user_data:
        raise ValueError(f"User with ID {userId} not found.")
    if not hasattr(user_data, "profile") or user_data.profile is None:
        raise ValueError(f"Profile details for User ID {userId} are missing.")
    response = GetUserProfileResponse(
        id=user_data.id,
        email=user_data.email,
        role=user_data.role,
        profile=UserProfile(
            firstName=user_data.profile.firstName,
            lastName=user_data.profile.lastName,
            contactNumber=user_data.profile.contactNumber,
        ),
    )
    return response
