-- CreateOrganizations
INSERT INTO organizations (organization_id, name, invite_code) 
VALUES (:organization_id, :name, :invite_code);

-- CreateUser
INSERT INTO users (user_id, username, hashed_password, role) 
VALUES (:user_id, :username, :hashed_password, :role);


-- FecthOrganizationByInviteCode
SELECT organization_id FROM organizations WHERE invite_code = :invite_code;


-- AddUserToOrganization
UPDATE users
SET organization_id = :organization_id
WHERE username = :username;


-- CreateCluster
INSERT INTO clusters (cluster_id, cluster_name, organization_id, total_cpu, total_ram, total_gpu, available_cpu, available_ram, available_gpu)
VALUES (:cluster_id, :cluster_name, :organization_id, :total_cpu, :total_ram, :total_gpu, :available_cpu, :available_ram, :available_gpu);

-- CreateDeployment
INSERT INTO deployments (deployment_id, user_id, cluster_id, image_path, required_cpu, required_ram, required_gpu, priority, status)
VALUES (:deployment_id, :user_id, :cluster_id, :image_path, :required_cpu, :required_ram, :required_gpu, :priority, :status);


-- GetUserDetails
SELECT user_id, username, hashed_password, role, organization_id from users where username = :username;


-- GetClusterDetails
SELECT available_cpu, available_ram, available_gpu FROM clusters WHERE cluster_id = :cluster_id;


-- DecreaseClusterResource
UPDATE clusters SET available_cpu = available_cpu - :available_cpu, available_ram = available_ram - :available_ram, available_gpu = available_gpu - :available_gpu WHERE cluster_id = :cluster_id;

-- UpdateDeploymentStatus
UPDATE deployments SET status = :status WHERE deployment_id = :deployment_id;

-- GetDeploymentDetailsByPriority
SELECT deployment_id, required_cpu, required_ram, required_gpu, priority FROM deployments WHERE cluster_id = :cluster_id AND status = :status ORDER BY priority ASC;


-- IncreaseClusterResource
UPDATE clusters SET available_cpu = available_cpu + :available_cpu, available_ram = available_ram + :available_ram, available_gpu = available_gpu + :available_gpu WHERE cluster_id = :cluster_id;
