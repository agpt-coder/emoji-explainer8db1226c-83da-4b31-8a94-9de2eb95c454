from pydantic import BaseModel


class ServerResourceUpdateResponse(BaseModel):
    """
    This model encapsulates the response after the server resource adjustments are made. It provides confirmation and the new state of the resources.
    """

    cpu_updated_allocation: float
    ram_updated_allocation: float
    disk_space_updated_allocation: float
    message: str


def updateServerResources(
    cpu_allocation_increment: float,
    ram_allocation_increment: float,
    disk_space_allocation_increment: float,
) -> ServerResourceUpdateResponse:
    """
    Through this PATCH route, Service Managers can update server resource allocations based on current demand and predictive data analytics from the Server Management module. The endpoint accepts parameters for resource adjustments and applies them immediately to maintain service quality.

    Args:
    cpu_allocation_increment (float): The increment or decrement value to adjust the CPU resources by, in percentage points. Positive values increase allocation, negative values decrease it.
    ram_allocation_increment (float): The increment or decrement value to adjust the RAM allocation by, in gigabytes. Positive values increase allocation, negative values decrease it.
    disk_space_allocation_increment (float): The increment or decrement value for adjusting the disk space by, in gigabytes. Positive values signify an increase, while negative values signify a decrease.

    Returns:
    ServerResourceUpdateResponse: This model encapsulates the response after the server resource adjustments are made. It provides confirmation and the new state of the resources.

    Example:
        updateServerResources(10, 5, 20)
        > ServerResourceUpdateResponse(
            cpu_updated_allocation=110, # assuming initial was 100%
            ram_updated_allocation=45, # assuming initial was 40GB
            disk_space_updated_allocation=220, # assuming initial was 200GB
            message="Server resources successfully updated."
          )
    """
    current_cpu = 100
    current_ram = 40
    current_disk = 200
    updated_cpu = current_cpu + cpu_allocation_increment
    updated_ram = current_ram + ram_allocation_increment
    updated_disk = current_disk + disk_space_allocation_increment
    return ServerResourceUpdateResponse(
        cpu_updated_allocation=updated_cpu,
        ram_updated_allocation=updated_ram,
        disk_space_updated_allocation=updated_disk,
        message="Server resources successfully updated.",
    )
