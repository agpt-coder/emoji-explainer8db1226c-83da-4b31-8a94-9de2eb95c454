from datetime import datetime

import prisma
import prisma.models
from pydantic import BaseModel


class LogoutResponse(BaseModel):
    """
    Model for the response of a logout operation. Indicates success or failure of the session invalidation.
    """

    message: str


async def logoutUser(token: str) -> LogoutResponse:
    """
    Logs out a user by invalidating their session token. Requires the current session token and responds with a success message upon successful logout.

    Args:
        token (str): The current session token that needs to be invalidated for logging the user out.

    Returns:
        LogoutResponse: Model for the response of a logout operation. Indicates success or failure of the session invalidation.

    Example:
        response = await logoutUser('some-session-token')
        if response:
            print(response.message)
        > 'User successfully logged out.'
    """
    try:
        session_id = int(token)
    except ValueError:
        return LogoutResponse(message="Invalid session token.")
    session = await prisma.models.Session.prisma().find_unique(where={"id": session_id})
    if not session:
        return LogoutResponse(message="No active session found for the given token.")
    if session.expiresAt < datetime.now():
        return LogoutResponse(message="prisma.models.Session already expired.")
    await prisma.models.Session.prisma().update(
        where={"id": session.id}, data={"expiresAt": datetime.now()}
    )
    return LogoutResponse(message="User successfully logged out.")
