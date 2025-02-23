# Hypervisor-like Service for MLOps Platform

This project implements user authentication, organization management, cluster creation, and deployment management using FastAPI, SQLite3, and JWT authentication. It also includes Docker support for easy deployment.


### Features

1. User Authentication

* Register & login users securely with JWT.
* Passwords are hashed using bcrypt.
* Users have a specific role (`admin`, `developer`, `viewer`)

2. Organization Management

* Users can join organizations using an invite code.

3. Cluster Management

* Users can create clusters with fixed resources (RAM, CPU, GPU).
* Only users with `admin` role can create new clusters.

4. Deployment Management

* Deployments are created with resource allocation.
* Only users having `admin` and`developer` role can create deployment.
* Automatic resource allocation
* Queue management for pending deployments
* Priority-based deployment scheduling
* Preemption support for high-priority workloads
* Includes a priority-based queuing system.

5. JWT-Based Security
* Protect API routes with authentication.


### Getting Started

#### Step: 1 Clone the Repository
```bash
git clone https://github.com/subhamyadav580/hypervisor-service
cd hypervisor-service
```

#### Step: 2 Build Image
```bash
docker-compose build
```


#### Step: 3 Start the service
```bash
docker-compose up -d
```

### Authentication Workflow

#### Create a Organization
Sample Request
```bash
curl --location --request GET 'http://localhost:8000/create_organization' \
--header 'Content-Type: application/json' \
--data '{
    "name": "dev-team"
}'
```
Sample Response
```bash
{"message":"organization created successfully","invite_code":"4wfvuKqjhZ"}
```

#### Register a User
Sample Request
```bash
curl --location 'http://localhost:8000/register' \
--header 'Content-Type: application/json' \
--data-raw '{
   "username" : "shubham",
   "password": "test@12345",
   "role": "admin"
}'
```
Sample Response
```bash
{"message":"user successfully created","username":"shubham"}
```


#### Join Organization by `invite_code`
Sample Request

`invite_code`: It will be recived when you will create a organization.
```bash
curl --location 'http://localhost:8000/join_organization' \
--header 'Content-Type: application/json' \
--data '{
    "invite_code": "4wfvuKqjhZ",
    "username": "shubham"
}'
```

Sample Response
```bash
{"message":"you have successfully joined the organization"}
```



#### Login and Get JWT Token
Sample Request
```bash
curl --location 'http://localhost:8000/login' \
--header 'Content-Type: application/json' \
--data-raw '{
   "username" : "shubham",
   "password": "test@12345"
}'
```
Sample Response
```bash
{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNGZjYzEzODctYmM5Ni00YTg5LTk3ODQtNGNkNDFlMjNjNDUxIiwib3JnYW5pemF0aW9uX2lkIjoiNTk3ODU3NDItMzk3OS00Y2I2LTgyYmEtMTVmODdjMGVkYTczIiwicm9sZSI6ImFkbWluIiwiZXhwIjoxNzQwMzE0ODcxfQ.QdQ5tu7njYdKVd3EVv8jAb63EjT91kjril6FBt7CTNU","token_type":"bearer","is_authorized":true}
```


#### Create a Cluster (Authenticated API)
Sample Request
```bash
curl --location 'http://localhost:8000/create_cluster' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNGZjYzEzODctYmM5Ni00YTg5LTk3ODQtNGNkNDFlMjNjNDUxIiwib3JnYW5pemF0aW9uX2lkIjoiNTk3ODU3NDItMzk3OS00Y2I2LTgyYmEtMTVmODdjMGVkYTczIiwicm9sZSI6ImFkbWluIiwiZXhwIjoxNzQwMzE0ODcxfQ.QdQ5tu7njYdKVd3EVv8jAb63EjT91kjril6FBt7CTNU' \
--header 'Content-Type: application/json' \
--data '{
    "cluster_name": "cluster-1",
    "total_cpu": 32,
    "total_ram":  64,
    "total_gpu": 2
}'
```
Sample Response
```bash
{"message":"cluster has been created successfully","cluster_id":"28ba2722-a17c-4dca-a46a-5925384aef16"}
```


#### Create a Deployment (Authenticated API)
Sample Request
```bash
curl --location 'http://localhost:8000/create_deployment' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNGZjYzEzODctYmM5Ni00YTg5LTk3ODQtNGNkNDFlMjNjNDUxIiwib3JnYW5pemF0aW9uX2lkIjoiNTk3ODU3NDItMzk3OS00Y2I2LTgyYmEtMTVmODdjMGVkYTczIiwicm9sZSI6ImFkbWluIiwiZXhwIjoxNzQwMzE0ODcxfQ.QdQ5tu7njYdKVd3EVv8jAb63EjT91kjril6FBt7CTNU' \
--header 'Content-Type: application/json' \
--data '{
    "cluster_id": "28ba2722-a17c-4dca-a46a-5925384aef16",
    "image_path": "tinyllama:latest",
    "required_cpu": 32,
    "required_ram": 48,
    "required_gpu": 0,
    "priority": 3
}'
```

Sample Response
```bash
{"message":"Deployment added to queue","deployment_id":"2ef2dbaf-b443-48bc-a577-5e9436c69522"}
```

### UML Diagram of DB
<img src="db_tables.png">

### UML Diagram of the service

<img src="service_uml.png">


