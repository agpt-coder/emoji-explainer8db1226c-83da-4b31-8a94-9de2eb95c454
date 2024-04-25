from pydantic import BaseModel


class EmojiStatusRequest(BaseModel):
    """
    Request model for the GET /api/emoji/status endpoint to provide service status without any input parameters.
    """

    pass


class EmojiStatusResponse(BaseModel):
    """
    A simple response model indicating the operational status of the emoji explanation service. Expected to return an HTTP 200 status if everything is functional.
    """

    status: str


def checkStatus(request: EmojiStatusRequest) -> EmojiStatusResponse:
    """
    Provides a heartbeat or status check of the emoji explanation service. This endpoint will simply return an HTTP 200 status if the service is active, indicating that the system is ready to receive and process emojis. This endpoint is crucial for service monitoring and alerting in case of system failures.

    Args:
        request (EmojiStatusRequest): Request model for the GET /api/emoji/status endpoint to provide service status without any input parameters.

    Returns:
        EmojiStatusResponse: A simple response model indicating the operational status of the emoji explanation service. Expected to return an HTTP 200 status if everything is functional.

    Example:
        status_request = EmojiStatusRequest()
        status_response = checkStatus(status_request)
        > {'status': 'Service is operational'}
    """
    service_operational = "Service is operational"
    return EmojiStatusResponse(status=service_operational)
