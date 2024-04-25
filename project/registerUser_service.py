from typing import Optional

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class UserRegistrationResponse(BaseModel):
    """
    This model packages the response after a successful user registration. It includes the new user's ID, indicating successful registration or an appropriate error message.
    """

    message: str
    user_id: Optional[int] = None
    error: Optional[str] = None


async def registerUser(
    username: str, password: str, email: str, role: Optional[prisma.enums.Role] = None
) -> UserRegistrationResponse:
    """
    This endpoint is used for registering a new user. It accepts user details such as username, password, and email. It returns a success message with a user ID if the registration is successful. Supports user role assignment during registration process if specified.

    Args:
        username (str): Desired username for the new account.
        password (str): Secure password for the new account. It should meet the complexity requirements set by the system's security policy.
        email (str): Email address for the user. This will be used for communication and password recovery where necessary.
        role (Optional[prisma.enums.Role]): The role assigned to the user at registration. If not provided, defaults to 'USER'.

    Returns:
        UserRegistrationResponse: This model packages the response after a successful user registration. It includes the new user's ID, indicating successful registration or an appropriate error message.
    """
    existing_user = await prisma.models.User.prisma().find_unique(
        where={"email": email}
    )
    if existing_user:
        return UserRegistrationResponse(
            message="Registration failed: Email already in use.",
            error="A user with this email already exists.",
        )
    final_role = role if role is not None else prisma.enums.Role.USER
    try:
        new_user = await prisma.models.User.prisma().create(
            data={
                "username": username,
                "password": password,
                "email": email,
                "role": final_role,
            }
        )
        return UserRegistrationResponse(
            message="User registered successfully.", user_id=new_user.id
        )
    except Exception as e:
        return UserRegistrationResponse(
            message="Registration failed due to an error.", error=str(e)
        )
