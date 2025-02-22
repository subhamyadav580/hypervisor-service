from pydantic import BaseModel

class RegisterUserRequest(BaseModel):
    username: str
    password: str
    role: str

class LoginUserRequest(BaseModel):
    username: str
    password: str

class CreateOrganizationRequest(BaseModel):
    name: str

class JoinOrganizationRequest(BaseModel):
    invite_code: str
    username: str

class CreateClusterRequest(BaseModel):
    cluster_name: str
    total_cpu: int
    total_ram: int
    total_gpu: int


class CreateDeploymentRequest(BaseModel):
    cluster_id: str
    image_path: str
    required_cpu: int
    required_ram: int
    required_gpu: int
    priority: int = 1
