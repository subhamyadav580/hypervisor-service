from fastapi import APIRouter, HTTPException, Depends
from models.request_models import (
    RegisterUserRequest, LoginUserRequest, CreateOrganizationRequest, 
    JoinOrganizationRequest, CreateClusterRequest, CreateDeploymentRequest
)
from services.user_service import (
    CreateUser, CreateOrganization, JoinOrganization, LoginUser
)
from services.cluster_service import (
    CreateCluster
)
from services.deployment_service import (
    CreateDeployment    
)

from services.auth import verify_token
import logging


# Initialize Logger
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/register")
async def register(body: RegisterUserRequest):
    """
    Registers a new user.
    Args:
        body (RegisterUserRequest): The registration request containing `username` and `password`.
    Returns:
        dict: A success message and the registered username.
    Raises:
        HTTPException: If user creation fails.
    """
    print("body:: ", body)
    username = body.username
    password = body.password
    try:
        username = CreateUser(username, password)
        print("username:: ", username)
        if not username:
            raise HTTPException(status_code=500, detail="User registration failed")
        return {"message": "success", "username": username}

    except Exception as e:
        logger.error(f"Error registering user: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/login")
def login(user: LoginUserRequest):
    """
    Logs in a user.
    Args:
        user (LoginUserRequest): The login request containing `username` and `password`.
    Returns:
        dict: Authentication response including authorization status and user details.
    Raises:
        HTTPException: If login credentials are invalid.
    """
    try:
        response = LoginUser(user.username, user.password)
        if not response or not response.get("is_authorized"):
            raise HTTPException(status_code=400, detail="Invalid credentials")
        return response
    except Exception as e:
        logger.error(f"Login failed for user {user.username}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")



@router.get("/create_organization")
async def create_organization(body: CreateOrganizationRequest):
    """
    Creates a new organization.
    Args:
        body (CreateOrganizationRequest): The request containing the organization's name.
    Returns:
        dict: A success message and an invite code for the organization.
    Raises:
        HTTPException: If organization creation fails.
    """
    try:
        invite_code = CreateOrganization(body.name)
        if not invite_code:
            raise HTTPException(status_code=500, detail="Failed to create organization")
        return {"message": "success", "invite_code": invite_code}
    except Exception as e:
        logger.error(f"Error creating organization: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/join_organization")
async def join_organization(body: JoinOrganizationRequest):
    """
    Allows a user to join an organization using an invite code.
    Args:
        body (JoinOrganizationRequest): The request containing `username` and `invite_code`.
    Returns:
        dict: Success or failure message.
    Raises:
        HTTPException: If joining the organization fails.
    """
    try:
        success = JoinOrganization(body.username, body.invite_code)
        if not success:
            raise HTTPException(status_code=400, detail="Invalid invite code or user does not exist")
        return {"message": "success"}
    except Exception as e:
        logger.error(f"Error joining organization: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.post("/create_cluster")
async def create_cluster(body: CreateClusterRequest, auth_data: dict = Depends(verify_token)):
    """
    Creates a new cluster for an authenticated user.
    Args:
        body (CreateClusterRequest): The request containing cluster details.
        auth_data (dict): Authentication data containing `user_id` and `organization_id`.
    Returns:
        dict: A success message with the created cluster ID or a failure message.
    Raises:
        HTTPException: If cluster creation fails.
    """
    try:
        user_id = auth_data.get("user_id")
        organization_id = auth_data.get("organization_id")
        if not user_id or not organization_id:
            raise HTTPException(status_code=401, detail="Unauthorized request")
        is_success, cluster_id = CreateCluster(body, user_id, organization_id)
        if not is_success:
            raise HTTPException(status_code=500, detail="Failed to create cluster")
        return {"message": "success", "cluster_id": cluster_id}
    except Exception as e:
        logger.error(f"Error creating cluster: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")



@router.post("/create_deployment")
async def create_deployment(body: CreateDeploymentRequest, auth_data: dict = Depends(verify_token)):
    """
    Creates a new deployment and adds it to the queue.
    Args:
        body (CreateDeploymentRequest): The request containing deployment details.
        auth_data (dict): Authentication data containing `user_id`.
    Returns:
        dict: A success message with deployment ID if added, otherwise a failure message.
    Raises:
        HTTPException: If deployment creation fails.
    """
    try:
        user_id = auth_data.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Unauthorized request")
        is_success, deployment_id = CreateDeployment(body, user_id)
        if not is_success:
            raise HTTPException(status_code=500, detail="Failed to create deployment")
        return {"message": "Deployment added to queue", "deployment_id": deployment_id}
    except Exception as e:
        logger.error(f"Error creating deployment: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
