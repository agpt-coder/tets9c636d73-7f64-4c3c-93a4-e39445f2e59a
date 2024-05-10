import bcrypt
import prisma
import prisma.models
from pydantic import BaseModel


class Role(BaseModel):
    """
    Enum representing various system roles.
    """

    role_value: str


class CreateUserProfileResponse(BaseModel):
    """
    Response model representing the result of a user creation request. It contains user ID and a status message.
    """

    user_id: int
    status: str


async def createUser(
    username: str, password: str, role: Role
) -> CreateUserProfileResponse:
    """
    Creates a new user profile in the system. This endpoint expects details such as username, password, and role. On success, it returns the user ID and a status message. It uses internal validation mechanisms to ensure data integrity.

    Args:
        username (str): The username for the new user. Must be unique across the system.
        password (str): The password for the new user. This will be hashed and stored securely in the database.
        role (Role): The role assigned to the new user. Must be one of the predefined roles in the system like SYSTEM_ADMINISTRATOR.

    Returns:
        CreateUserProfileResponse: Response model representing the result of a user creation request. It contains user ID and a status message.

    Example:
        role = Role(role_value="SYSTEM_ADMINISTRATOR")
        createUser("new_user", "securePassword123", role)
        > CreateUserProfileResponse(user_id=123, status="User created successfully")
    """
    existing_user = await prisma.models.User.prisma().find_unique(
        where={"email": username}
    )
    if existing_user is not None:
        return CreateUserProfileResponse(user_id=0, status="Username already exists")
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode(
        "utf-8"
    )
    user = await prisma.models.User.prisma().create(
        data={
            "email": username,
            "hashedPassword": hashed_password,
            "role": role.role_value,
        }
    )
    return CreateUserProfileResponse(
        user_id=user.id, status="User created successfully"
    )
