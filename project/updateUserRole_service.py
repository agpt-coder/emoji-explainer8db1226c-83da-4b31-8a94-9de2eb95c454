import prisma
import prisma.models
from pydantic import BaseModel


class UserRoleUpdateResponse(BaseModel):
    """
    Response model for updating a user role. Confirms the updated details along with the user id for reference.
    """

    userId: int
    updatedRole: str
    status: str


async def updateUserRole(userId: int, newRole: str) -> UserRoleUpdateResponse:
    """
    Updates the role of a specific user. This is typically used by administrators to elevate privileges or change user roles. Requires admin privileges and the targeted user's ID along with the new role.

    Args:
        userId (int): The unique identifier of the user whose role is to be updated.
        newRole (str): The new role that the user will be assigned. Must be one of the predefined 'Role' enum values.

    Returns:
        UserRoleUpdateResponse: Response model for updating a user role. Confirms the updated details along with the user id for reference.

    Example:
        updated_user = await updateUserRole(3, 'ADMIN')
        print(updated_user)
        > UserRoleUpdateResponse(userId=3, updatedRole='ADMIN', status='Success')
    """
    user = await prisma.models.User.prisma().find_unique(where={"id": userId})
    if not user:
        return UserRoleUpdateResponse(
            userId=userId, updatedRole="", status="User not found"
        )
    updated_user = await prisma.models.User.prisma().update(
        where={"id": userId}, data={"role": newRole}
    )
    return UserRoleUpdateResponse(userId=userId, updatedRole=newRole, status="Success")
