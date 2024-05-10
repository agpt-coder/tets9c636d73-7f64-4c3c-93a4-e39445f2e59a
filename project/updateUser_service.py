from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class Role(BaseModel):
    """
    Enum representing various system roles.
    """

    role_value: str


class UserUpdateResponse(BaseModel):
    """
    This model returns the updated information of the user after the successful operation. It confirms the changes and provides the current state of the user data.
    """

    userId: int
    name: str
    email: str
    role: Role


async def updateUser(
    userId: int, name: Optional[str], email: Optional[str], role: Optional[Role]
) -> UserUpdateResponse:
    """
    Asynchronously updates user information such as name, email, or role based on the provided user ID.
    This function interfaces with the database to make updates and ensures that the updates meet business rules.

    Args:
        userId (int): The ID of the user to update.
        name (Optional[str]): Optional new name for the user if a change is desired.
        email (Optional[str]): Optional new email for the user if a change is desired. Must be unique.
        role (Optional[Role]): Optional new role for the user if a change is desired.

    Returns:
        UserUpdateResponse: An object containing the updated user information.

    Raises:
        ValueError: If the given user ID does not exist.
    """
    user = await prisma.models.User.prisma().find_unique(
        where={"id": userId}, include={"profile": True}
    )
    if not user:
        raise ValueError("User ID not found")
    update_data = {}
    if name is not None:
        names = name.split(" ")
        first_name, last_name = (
            names[0],
            " ".join(names[1:]) if len(names) > 1 else "",
        )
        update_data["profile"] = {
            "update": {"firstName": first_name, "lastName": last_name}
        }
    if email is not None:
        update_data["email"] = email
    if role is not None:
        update_data["role"] = role
    updated_user = await prisma.models.User.prisma().update(
        where={"id": userId}, data=update_data, include={"profile": True}
    )
    return UserUpdateResponse(
        userId=updated_user.id,
        name=f"{updated_user.profile.firstName} {updated_user.profile.lastName}"
        if updated_user.profile
        else None,
        email=updated_user.email,
        role=updated_user.role,
    )
