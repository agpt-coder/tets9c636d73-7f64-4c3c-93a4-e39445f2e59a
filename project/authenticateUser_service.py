from datetime import datetime, timedelta

import bcrypt
import prisma
import prisma.models
from jose import jwt
from pydantic import BaseModel


class Role(BaseModel):
    """
    Enum representing various system roles.
    """

    role_value: str


class UserLoginResponse(BaseModel):
    """
    Response model for a successful user login, which includes the access token and potentially basic user information.
    """

    token: str
    userId: int
    role: enum[Role]  # TODO(autogpt): F821 Undefined name `enum`


SECRET_KEY = "YOUR_SECRET_KEY_HERE"


async def authenticateUser(username: str, password: str) -> UserLoginResponse:
    """
    Handles user login by authenticating username and password. On successful authentication, it returns a token used for session management and further requests. This is a critical endpoint for ensuring secure access across various system roles.

    Args:
        username (str): The username for the user attempting to log in.
        password (str): The password for the user attempting to log in.

    Returns:
        UserLoginResponse: Response model for a successful user login, which includes the access token and potentially basic user information.

    Example:
        response = await authenticateUser('example@domain.com', 'correctpassword123')
        print(response.token, response.userId, response.role)
    """
    user = await prisma.models.User.prisma().find_unique(where={"email": username})
    if user and bcrypt.checkpw(
        password.encode("utf-8"), user.hashedPassword.encode("utf-8")
    ):
        claims = {
            "sub": str(user.id),
            "role": user.role.name,
            "exp": datetime.utcnow() + timedelta(hours=1),
        }
        token = jwt.encode(claims, SECRET_KEY, algorithm="HS256")
        return UserLoginResponse(token=token, userId=user.id, role=user.role.name)
    else:
        raise Exception("Invalid username or password")
