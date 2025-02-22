from models.request_models import CreateClusterRequest
from db.repo import ExecuteQueryInDB, get_query_from_sql_file
import uuid


def CreateCluster(cluster_request: CreateClusterRequest, user_id, organization_id):
    params = {
        "user_id": user_id,
        "organization_id": organization_id,
        "cluster_id": str(uuid.uuid4()),
        "cluster_name": cluster_request.cluster_name,
        "total_cpu": cluster_request.total_cpu,
        "total_ram": cluster_request.total_ram,
        "total_gpu": cluster_request.total_gpu,
        "available_cpu": cluster_request.total_cpu,
        "available_ram": cluster_request.total_ram,
        "available_gpu": cluster_request.total_gpu
    }
    print(params)
    query = get_query_from_sql_file("CreateCluster")
    if ExecuteQueryInDB(query, params):
        return True, params["cluster_id"]
    else:
        return False, ""
        

