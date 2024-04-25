from datetime import datetime

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class SessionVerifyResponse(BaseModel):
    """
    Response model for the session verification process. It will indicate whether the session token is valid or not.
    """

    is_valid: bool
    user_role: prisma.enums.Role


class Role(BaseModel):
    ADMIN: str = "ADMIN"
    USER: str = "USER"
    SERVICE_MANAGER: str = "SERVICE_MANAGER"


async def verifySession(session_token: str) -> SessionVerifyResponse:
    """
    Verifies the validity of a user's session token. It is used by various modules to ensure that user requests are authenticated. The endpoint checks the provided session token and returns the validation status.

    Args:
        session_token (str): The session token that needs to be verified to ensure it's valid and active.

    Returns:
        SessionVerifyResponse: Response model for the session verification process. It will indicate whether the session token is valid or not.
    """
    session = await prisma.models.Session.prisma().find_unique(
        where={"id": int(session_token)}
    )
    if session and session.expiresAt >= datetime.now():
        user = await prisma.models.User.prisma().find_unique(
            where={"id": session.userId}
        )
        return SessionVerifyResponse(is_valid=True, user_role=user.role)
    else:
        return SessionVerifyResponse(is_valid=False, user_role=None)
