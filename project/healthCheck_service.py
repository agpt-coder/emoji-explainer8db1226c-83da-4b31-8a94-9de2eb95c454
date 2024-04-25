from datetime import datetime

from pydantic import BaseModel


class HealthCheckRequest(BaseModel):
    """
    Request for checking the health of the Explanation Processor module. No input parameters needed as this is a basic GET request.
    """

    pass


class HealthCheckResponse(BaseModel):
    """
    Response that indicates the health status of the Explanation Processor module. Primarily used by the service manager for monitoring.
    """

    status: str
    timestamp: str
    message: str


def healthCheck(request: HealthCheckRequest) -> HealthCheckResponse:
    """
    A simple health check endpoint for monitoring the status of the Explanation Processor module.
    Responds with a 200 OK status if the module is functioning correctly, otherwise it will generate
    relevant error statuses. This is crucial for ongoing maintenance and monitoring by the Service Manager role.

    Args:
        request (HealthCheckRequest): Request for checking the health of the Explanation Processor module.
                                      No input parameters needed as this is a basic GET request.

    Returns:
        HealthCheckResponse: Response that indicates the health status of the Explanation Processor module.
                             Primarily used by the service manager for monitoring.

    Example:
        request = HealthCheckRequest()
        response = healthCheck(request)
        # HealthCheckResponse(status='OK', timestamp='2023-10-10T10:00:00', message='Service is up and running.')
    """
    time_now = datetime.now().isoformat()
    try:
        return HealthCheckResponse(
            status="OK", timestamp=time_now, message="Service is up and running."
        )
    except Exception as error:
        return HealthCheckResponse(
            status="ERROR",
            timestamp=time_now,
            message=f"Service check failed: {str(error)}",
        )
