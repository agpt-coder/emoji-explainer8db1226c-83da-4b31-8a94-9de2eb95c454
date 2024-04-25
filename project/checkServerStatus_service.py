from datetime import datetime

import psutil
from pydantic import BaseModel


class ServerStatusRequest(BaseModel):
    """
    Request model for fetching server status. Since this is a GET request, no body is required, and if any parameters are needed, they would typically be in the query string. This example assumes no parameters are needed.
    """

    pass


class ServerStatusResponse(BaseModel):
    """
    Provides detailed information about server resources and performance to service managers for scalable deployment and efficient load management.
    """

    cpu_utilization: float
    memory_utilization: float
    disk_space_remaining: float
    network_status: str
    last_update_time: datetime


def checkServerStatus(request: ServerStatusRequest) -> ServerStatusResponse:
    """
    This GET endpoint provides an overview of the current server status and resource utilization, meant primarily for internal monitoring and adjustment by Service Managers. It aids in scalable deployment by offering real-time data critical for efficient performance tweaking.

    Args:
        request (ServerStatusRequest): Request model for fetching server status. Since this is a GET request, no body is required, and if any parameters are needed, they would typically be in the query string. This example assumes no parameters are needed.

    Returns:
        ServerStatusResponse: Provides detailed information about server resources and performance to service managers for scalable deployment and efficient load management.

    Example:
        request = ServerStatusRequest()
        response = checkServerStatus(request)
        # Output would include fields like CPU utilization, memory utilization, etc.
    """
    memory = psutil.virtual_memory()
    memory_util_in_gb = memory.used / 1024**3
    disk = psutil.disk_usage("/")
    disk_space_remaining_gb = disk.free / 1024**3
    cpu_util = psutil.cpu_percent(interval=1)
    network_status = "healthy"
    last_update = datetime.now()
    return ServerStatusResponse(
        cpu_utilization=cpu_util,
        memory_utilization=memory_util_in_gb,
        disk_space_remaining=disk_space_remaining_gb,
        network_status=network_status,
        last_update_time=last_update,
    )
