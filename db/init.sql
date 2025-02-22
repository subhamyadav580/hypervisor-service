CREATE TABLE IF NOT EXISTS organizations (
    organization_id varchar(255) PRIMARY KEY, 
    name TEXT UNIQUE NOT NULL,
    invite_code TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    user_id varchar(255) PRIMARY KEY, 
    username TEXT UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('admin', 'developer', 'viewer')),
    organization_id varchar(255),
    FOREIGN KEY (organization_id) REFERENCES organizations (organization_id)
);


CREATE TABLE IF NOT EXISTS clusters (
    cluster_id varchar(255) PRIMARY KEY,
    cluster_name TEXT UNIQUE NOT NULL,
    organization_id varchar(255),
    total_cpu INTEGER NOT NULL,
    total_ram INTEGER NOT NULL,
    total_gpu INTEGER NOT NULL,
    available_cpu INTEGER NOT NULL,
    available_ram INTEGER NOT NULL,
    available_gpu INTEGER NOT NULL,
    FOREIGN KEY (organization_id) REFERENCES organizations (organization_id)
);


CREATE TABLE IF NOT EXISTS deployments (
    deployment_id varchar(255) PRIMARY KEY,
    user_id varchar(255),
    cluster_id varchar(255),
    image_path TEXT NOT NULL,
    required_cpu INTEGER NOT NULL,
    required_ram INTEGER NOT NULL,
    required_gpu INTEGER NOT NULL,
    priority INTEGER NOT NULL DEFAULT 1,
    status TEXT NOT NULL DEFAULT 'QUEUED',
    FOREIGN KEY (user_id) REFERENCES users (user_id),
    FOREIGN KEY (cluster_id) REFERENCES clusters (cluster_id)
);
