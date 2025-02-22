# Hypervisor-like Service for MLOps Platform

This project implements user authentication, organization management, cluster creation, and deployment management using FastAPI, SQLite3, and JWT authentication. It also includes Docker support for easy deployment.


### Features

1. User Authentication

* Register & login users securely with JWT.
* Passwords are hashed using bcrypt.

2. Organization Management

* Users can join organizations using an invite code.

3. Cluster Management

* Users can create clusters with fixed resources (RAM, CPU, GPU).

4. Deployment Management

* Deployments are created with resource allocation.

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
{"message":"success","invite_code":"U4wwp2b3SZ"}
```

#### Register a User
Sample Request
```bash
curl --location 'http://localhost:8000/register' \
--header 'Content-Type: application/json' \
--data-raw '{
   "username" : "test_user",
   "password": "test@12345"
}'
```
Sample Response
```bash
{"message":"success","username":"test_user"}
```


#### Join Organization by `invite_code`
Sample Request

`invite_code`: It will be recived when you will create a organization.
```bash
curl --location 'http://localhost:8000/join_organization' \
--header 'Content-Type: application/json' \
--data '{
    "invite_code": "U4wwp2b3SZ",
    "username": "test_user"
}'
```

Sample Response
```bash
{"message":"success"}
```



#### Login and Get JWT Token
Sample Request
```bash
curl --location 'http://localhost:8000/login' \
--header 'Content-Type: application/json' \
--data-raw '{
   "username" : "test_user",
   "password": "test@12345"
}'
```
Sample Response
```bash
{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiY2FjMzNmNGYtNzhkNy00ZDEyLWIxYTAtOWQ2ZGY2ODIyMjJlIiwib3JnYW5pemF0aW9uX2lkIjoiYzg5NmJiYzktNTk0MC00MjA3LTk3ZmEtZmYzYjhhZDlkNjVmIiwiZXhwIjoxNzQwMjcxNjY2fQ.-K02PGV8xkrCSTPkihud2Tdhe2k5s5NsHpecAX23W1Y","token_type":"bearer","is_authorized":true}
```


#### Create a Cluster (Authenticated API)
Sample Request
```bash
curl --location 'http://localhost:8000/create_cluster' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiY2FjMzNmNGYtNzhkNy00ZDEyLWIxYTAtOWQ2ZGY2ODIyMjJlIiwib3JnYW5pemF0aW9uX2lkIjoiYzg5NmJiYzktNTk0MC00MjA3LTk3ZmEtZmYzYjhhZDlkNjVmIiwiZXhwIjoxNzQwMjcxNjY2fQ.-K02PGV8xkrCSTPkihud2Tdhe2k5s5NsHpecAX23W1Y' \
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
{"message":"sucess","cluster_id":"4e171f79-1009-4830-809c-ca95fc584245"}
```


#### Create a Deployment (Authenticated API)
Sample Request
```bash
curl --location 'http://localhost:8000/create_deployment' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiY2FjMzNmNGYtNzhkNy00ZDEyLWIxYTAtOWQ2ZGY2ODIyMjJlIiwib3JnYW5pemF0aW9uX2lkIjoiYzg5NmJiYzktNTk0MC00MjA3LTk3ZmEtZmYzYjhhZDlkNjVmIiwiZXhwIjoxNzQwMjcxNjY2fQ.-K02PGV8xkrCSTPkihud2Tdhe2k5s5NsHpecAX23W1Y' \
--header 'Content-Type: application/json' \
--data '{
    "cluster_id": "4e171f79-1009-4830-809c-ca95fc584245",
    "image_path": "tinyllama:latest",
    "required_cpu": 1,
    "required_ram": 20,
    "required_gpu": 0,
    "priority": 4
}'
```

Sample Response
```bash
{"message":"Deployment added to queue","deployment_id":"bd86c8e6-d210-419f-b1b5-4524f3e16b68"}
```




