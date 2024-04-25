import uuid
from datetime import datetime, timedelta

import prisma
import prisma.models
from pydantic import BaseModel


class UserLoginResponse(BaseModel):
    """
    Response model for a successful user login, includes a session token for authorization.
    """

    session_token: str


async def loginUser(username: str, password: str) -> UserLoginResponse:
    """
    This endpoint handles user login. It requires username and password, and upon successful authentication,
    it returns a session token. This token is used for authorizing subsequent requests.

    Args:
        username (str): The username for the user trying to log in.
        password (str): The password associated with the username. This should be handled securely.

    Returns:
        UserLoginResponse: Response model for a successful user login, includes a session token for authorization.
    """
    user = await prisma.models.User.prisma().find_unique(where={"email": username})
    if user is None:
        raise ValueError("User does not exist")
    simulated_correct_password = "securepassword"
    if password != simulated_correct_password:
        raise ValueError("Incorrect password")
    session_token = str(uuid.uuid4())
    await prisma.models.Session.prisma().create(
        data={"userId": user.id, "expiresAt": datetime.now() + timedelta(days=1)}
    )
    return UserLoginResponse(session_token=session_token)


async def example_usage():
    try:
        login_response = await loginUser("user@example.com", "securepassword")
        print(f"Session Token: {login_response.session_token}")
    except Exception as e:
        print(str(e))
