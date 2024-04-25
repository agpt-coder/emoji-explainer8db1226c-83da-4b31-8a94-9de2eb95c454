import logging
from contextlib import asynccontextmanager
from typing import Optional

import prisma
import prisma.enums
import project.checkServerStatus_service
import project.checkStatus_service
import project.deleteResourceAllocation_service
import project.explainEmoji_service
import project.healthCheck_service
import project.loginUser_service
import project.logoutUser_service
import project.receiveEmoji_service
import project.registerUser_service
import project.updateServerResources_service
import project.updateUserRole_service
import project.verifySession_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="emoji explainer",
    lifespan=lifespan,
    description="create an endpoint that takes an emoji as an input and returns it's explaination.  Use Groq, specifically llama3 for the explanaition",
)


@app.post(
    "/emoji/explain",
    response_model=project.explainEmoji_service.EmojiExplanationResponse,
)
async def api_post_explainEmoji(
    emoji: str,
) -> project.explainEmoji_service.EmojiExplanationResponse | Response:
    """
    Receives an emoji via POST request and returns its explanation. The emoji is validated by the Input Handler before being processed. This route utilizes the llama3 technology from Groq to fetch the explanation. The expected response is a JSON object containing the original emoji and its explanation. The route is designed to handle requests efficiently, ensuring that the emoji is valid and delegating processing power requisition to Server Management.
    """
    try:
        res = await project.explainEmoji_service.explainEmoji(emoji)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/api/emoji/status", response_model=project.checkStatus_service.EmojiStatusResponse
)
async def api_get_checkStatus(
    request: project.checkStatus_service.EmojiStatusRequest,
) -> project.checkStatus_service.EmojiStatusResponse | Response:
    """
    Provides a heartbeat or status check of the emoji explanation service. This endpoint will simply return an HTTP 200 status if the service is active, indicating that the system is ready to receive and process emojis. This endpoint is crucial for service monitoring and alerting in case of system failures.
    """
    try:
        res = project.checkStatus_service.checkStatus(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/health", response_model=project.healthCheck_service.HealthCheckResponse)
async def api_get_healthCheck(
    request: project.healthCheck_service.HealthCheckRequest,
) -> project.healthCheck_service.HealthCheckResponse | Response:
    """
    A simple health check endpoint for monitoring the status of the Explanation Processor module. Responds with a 200 OK status if the module is functioning correctly, otherwise it will generate relevant error statuses. This is crucial for ongoing maintenance and monitoring by the Service Manager role.
    """
    try:
        res = project.healthCheck_service.healthCheck(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/api/emoji/receive", response_model=project.receiveEmoji_service.EmojiResponseModel
)
async def api_post_receiveEmoji(
    emoji: str,
) -> project.receiveEmoji_service.EmojiResponseModel | Response:
    """
    Receives an emoji character from a user, validates it to ensure it's a proper emoji, and sends it to the Explanation Processor module. The emoji should be a valid Unicode character recognized as an emoji. If the validation is successful, the emoji is sent using an internal API call to Groq's llama3 for further explanation. The route should be able to handle a JSON request containing the emoji and respond with either a success or an error message detailing the validation outcome.
    """
    try:
        res = await project.receiveEmoji_service.receiveEmoji(emoji)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/api/server/resource",
    response_model=project.deleteResourceAllocation_service.DeleteResourceResponse,
)
async def api_delete_deleteResourceAllocation(
    resource_id: str,
) -> project.deleteResourceAllocation_service.DeleteResourceResponse | Response:
    """
    This DELETE endpoint is used by Service Managers to remove specific resource allocations which are no longer necessary. It helps in optimizing the resource usage of the server, ensuring efficient operation of the Explanation Processor by freeing up unused resources.
    """
    try:
        res = await project.deleteResourceAllocation_service.deleteResourceAllocation(
            resource_id
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/users/logout", response_model=project.logoutUser_service.LogoutResponse)
async def api_post_logoutUser(
    token: str,
) -> project.logoutUser_service.LogoutResponse | Response:
    """
    Logs out a user by invalidating their session token. Requires the current session token and responds with a success message upon successful logout.
    """
    try:
        res = await project.logoutUser_service.logoutUser(token)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/api/server/status",
    response_model=project.checkServerStatus_service.ServerStatusResponse,
)
async def api_get_checkServerStatus(
    request: project.checkServerStatus_service.ServerStatusRequest,
) -> project.checkServerStatus_service.ServerStatusResponse | Response:
    """
    This GET endpoint provides an overview of the current server status and resource utilization, meant primarily for internal monitoring and adjustment by Service Managers. It aids in scalable deployment by offering real-time data critical for efficient performance tweaking.
    """
    try:
        res = project.checkServerStatus_service.checkServerStatus(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/users/role/update",
    response_model=project.updateUserRole_service.UserRoleUpdateResponse,
)
async def api_put_updateUserRole(
    userId: int, newRole: str
) -> project.updateUserRole_service.UserRoleUpdateResponse | Response:
    """
    Updates the role of a specific user. This is typically used by administrators to elevate privileges or change user roles. Requires admin privileges and the targeted user's ID along with the new role.
    """
    try:
        res = await project.updateUserRole_service.updateUserRole(userId, newRole)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.patch(
    "/api/server/update",
    response_model=project.updateServerResources_service.ServerResourceUpdateResponse,
)
async def api_patch_updateServerResources(
    cpu_allocation_increment: float,
    ram_allocation_increment: float,
    disk_space_allocation_increment: float,
) -> project.updateServerResources_service.ServerResourceUpdateResponse | Response:
    """
    Through this PATCH route, Service Managers can update server resource allocations based on current demand and predictive data analytics from the Server Management module. The endpoint accepts parameters for resource adjustments and applies them immediately to maintain service quality.
    """
    try:
        res = project.updateServerResources_service.updateServerResources(
            cpu_allocation_increment,
            ram_allocation_increment,
            disk_space_allocation_increment,
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/users/register",
    response_model=project.registerUser_service.UserRegistrationResponse,
)
async def api_post_registerUser(
    username: str, password: str, email: str, role: Optional[prisma.enums.Role]
) -> project.registerUser_service.UserRegistrationResponse | Response:
    """
    This endpoint is used for registering a new user. It accepts user details such as username, password, and email. It returns a success message with a user ID if the registration is successful. Supports user role assignment during registration process if specified.
    """
    try:
        res = await project.registerUser_service.registerUser(
            username, password, email, role
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/users/session/verify",
    response_model=project.verifySession_service.SessionVerifyResponse,
)
async def api_get_verifySession(
    session_token: str,
) -> project.verifySession_service.SessionVerifyResponse | Response:
    """
    Verifies the validity of a user's session token. It is used by various modules to ensure that user requests are authenticated. The endpoint checks the provided session token and returns the validation status.
    """
    try:
        res = await project.verifySession_service.verifySession(session_token)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/users/login", response_model=project.loginUser_service.UserLoginResponse)
async def api_post_loginUser(
    username: str, password: str
) -> project.loginUser_service.UserLoginResponse | Response:
    """
    This endpoint handles user login. It requires username and password, and upon successful authentication, it returns a session token. This token is used for authorizing subsequent requests.
    """
    try:
        res = await project.loginUser_service.loginUser(username, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
