import prisma
import prisma.models
from pydantic import BaseModel


class DeleteResourceResponse(BaseModel):
    """
    Defines the response after attempting to delete a server resource, providing either a success confirmation or details on why deletion failed.
    """

    message: str


async def deleteResourceAllocation(resource_id: str) -> DeleteResourceResponse:
    """
    This DELETE endpoint is used by Service Managers to remove specific resource allocations which are no longer necessary. It helps in optimizing the resource usage of the server, ensuring efficient operation of the Explanation Processor by freeing up unused resources.

    Args:
    resource_id (str): The unique identifier of the resource to be deleted.

    Returns:
    DeleteResourceResponse: Defines the response after attempting to delete a server resource, providing either a success confirmation or details on why deletion failed.
    """
    try:
        explanation = await prisma.models.Explanation.prisma().delete(
            where={"id": resource_id}
        )
        if explanation:
            return DeleteResourceResponse(
                message="Resource allocation deleted successfully."
            )
        else:
            return DeleteResourceResponse(message="Resource allocation not found.")
    except Exception as e:
        return DeleteResourceResponse(
            message=f"Failed to delete resource allocation: {str(e)}"
        )
