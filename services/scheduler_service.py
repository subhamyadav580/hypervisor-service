from db.repo import (
    GetRedisData, get_query_from_sql_file,
    FetchOneInDB, RemoveFromRedis, ExecuteQueryInDB,
    FetchAllFromDB, SetDataInRedis
)
import time
import json


def scheduler_worker():
    print("start")
    while True:
        print("From redis")
        deployment_data = GetRedisData()
        print("deployment_data: ", deployment_data)
        if not deployment_data:
            time.sleep(5)  # Wait if queue is empty
            continue

        deployment_json, priority = deployment_data[0]
        deployment = json.loads(deployment_json)
        print("deployment data:: ", deployment)

        cluster_id = deployment["cluster_id"]
        required_cpu = deployment["required_cpu"]
        required_ram = deployment["required_ram"]
        required_gpu = deployment["required_gpu"]
        deployment_id = deployment["deployment_id"]

        # Fetch cluster details
        get_cluster_query = get_query_from_sql_file("GetClusterDetails")
        print("cluster_id:: ", cluster_id)
        cluster_data = FetchOneInDB(get_cluster_query, {"cluster_id": cluster_id})
        print("cluster_data:: ", cluster_data)

        if not cluster_data:
            RemoveFromRedis(deployment_json)
            continue

        available_cpu = cluster_data["available_cpu"]
        available_ram = cluster_data["available_ram"]
        available_gpu = cluster_data["available_gpu"]
        print(available_cpu,required_cpu ,"-", available_ram , required_ram ,"-", available_gpu , required_gpu)
        # Check if resources are available
        if available_cpu >= required_cpu and available_ram >= required_ram and available_gpu >= required_gpu:
            update_cluster_query = get_query_from_sql_file("DecreaseClusterResource")
            update_deployment_query = get_query_from_sql_file("UpdateDeploymentStatus")
            # Allocate resources
            ExecuteQueryInDB(update_cluster_query, {
                "available_cpu": required_cpu,
                "available_ram": required_ram,
                "available_gpu": required_gpu,
                "cluster_id": cluster_id
            })
            ExecuteQueryInDB(update_deployment_query, {
                "status": "RUNNING",
                "deployment_id": deployment_id
            })

            # Remove from queue
            RemoveFromRedis(deployment_json)
            print(f"Deployment {deployment_id} started in cluster {cluster_id}")

        else:
            get_running_deployment_query = get_query_from_sql_file("GetDeploymentDetailsByPriority")
            running_deployments = FetchAllFromDB(get_running_deployment_query, {
                "cluster_id": cluster_id,
                "status": "RUNNING"
            })

            freed_cpu, freed_ram, freed_gpu = 0, 0, 0
            stopped_deployments = []

            for deployment_dict in running_deployments:
                run_dep_id = deployment_dict["deployment_id"]
                run_cpu = deployment_dict["required_cpu"]
                run_ram = deployment_dict["required_ram"]
                run_gpu = deployment_dict["required_gpu"]
                run_priority = deployment_dict["priority"]
                print("run_priority: priority", run_priority, priority)


                if run_priority < priority:
                    update_deployment_query = get_query_from_sql_file("UpdateDeploymentStatus")
                    increase_cluster_resource_query = get_query_from_sql_file("IncreaseClusterResource")

                    ExecuteQueryInDB(update_deployment_query, {
                        "status": "PAUSED",
                        "deployment_id": run_dep_id
                    })
                    ExecuteQueryInDB(increase_cluster_resource_query, {
                        "available_cpu": run_cpu,
                        "available_ram": run_ram,
                        "available_gpu": run_gpu,
                        "cluster_id": cluster_id
                    })

                    freed_cpu += run_cpu
                    freed_ram += run_ram
                    freed_gpu += run_gpu
                    stopped_deployments.append(run_dep_id)

                    # **Requeue paused deployment in Redis**
                    paused_deployment_data = {
                        "cluster_id": cluster_id,
                        "required_cpu": run_cpu,
                        "required_ram": run_ram,
                        "required_gpu": run_gpu,
                        "deployment_id": run_dep_id,
                        "priority": run_priority
                    }
                    SetDataInRedis(paused_deployment_data, run_priority)  # Requeue task

                    # Check if we've freed enough resources
                    if (available_cpu + freed_cpu) >= required_cpu and \
                       (available_ram + freed_ram) >= required_ram and \
                       (available_gpu + freed_gpu) >= required_gpu:
                        break  # Stop when enough resources are freed

            # If enough resources are freed, start the high-priority deployment
            if (available_cpu + freed_cpu) >= required_cpu and \
               (available_ram + freed_ram) >= required_ram and \
               (available_gpu + freed_gpu) >= required_gpu:
                decrease_cluster_resource_query = get_query_from_sql_file("DecreaseClusterResource")
                
                ExecuteQueryInDB(decrease_cluster_resource_query, {
                    "available_cpu": required_cpu,
                    "available_ram": required_ram,
                    "available_gpu": required_gpu,
                    "cluster_id": cluster_id
                })
                ExecuteQueryInDB(update_deployment_query, {
                    "status": "RUNNING",
                    "deployment_id": deployment_id
                })
                RemoveFromRedis(deployment_json)
                print(f"Deployment {deployment_id} preempted {stopped_deployments} and started in cluster {cluster_id}")

        time.sleep(2)  # Prevent excessive polling
