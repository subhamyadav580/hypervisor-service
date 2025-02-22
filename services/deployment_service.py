from models.request_models import CreateDeploymentRequest
from db.repo import ExecuteQueryInDB, get_query_from_sql_file, SetDataInRedis
import uuid

def CreateDeployment(deployment_request: CreateDeploymentRequest, user_id):
    params = {
        "user_id": user_id,
        "deployment_id": str(uuid.uuid4()),
        "cluster_id": deployment_request.cluster_id,
        "image_path": deployment_request.image_path,
        "required_cpu": deployment_request.required_cpu,
        "required_ram": deployment_request.required_ram,
        "required_gpu": deployment_request.required_gpu,
        "priority": deployment_request.priority,
        "status": "queued"
    }
    print(params)
    query = get_query_from_sql_file("CreateDeployment")
    if ExecuteQueryInDB(query, params):
            dataToInsertInQueue = {
                "deployment_id": params["deployment_id"],
                "cluster_id": deployment_request.cluster_id,
                "required_cpu": deployment_request.required_cpu,
                "required_ram": deployment_request.required_ram,
                "required_gpu": deployment_request.required_gpu,
                "priority": deployment_request.priority
            }
            SetDataInRedis(dataToInsertInQueue, priority=deployment_request.priority)
            return True, params["deployment_id"]
    else:
        return False, ""
