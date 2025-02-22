from db.connection import get_db_connection
from db.repo import get_query_from_sql_file, ExecuteQueryInDB, FetchOneInDB
import uuid
import secrets
import string
from services.auth import pwd_context, create_access_token, verify_token


def CreateOrganization(organization):
    query = get_query_from_sql_file("CreateOrganizations")
    characters = string.ascii_letters + string.digits
    invite_code = ''.join(secrets.choice(characters) for _ in range(10))
    params = {
        "organization_id": str(uuid.uuid4()),
        "name": organization,
        "invite_code": invite_code
    }
    ExecuteQueryInDB(query, params)
    return params["invite_code"]


def CreateUser(username, password):
    print("Userna,e", username, password)
    query = get_query_from_sql_file("CreateUser")
    hashed_password = pwd_context.hash(password)
    params = {
        "user_id": str(uuid.uuid4()),
        "username": username,
        "hashed_password": hashed_password
    }
    print("Query", params)
    if ExecuteQueryInDB(query, params):
        return params["username"]
    else:
        return ""


def JoinOrganization(username, invite_code):
    invite_query = get_query_from_sql_file("FecthOrganizationByInviteCode")
    assign_query = get_query_from_sql_file("AddUserToOrganization")
    params = {
        "invite_code": invite_code
    }
    organization_data = FetchOneInDB(invite_query, params)
    if not organization_data:
        return False
    params["organization_id"] = organization_data["organization_id"]
    params["username"] = username
    return ExecuteQueryInDB(assign_query, params)



def LoginUser(username, password):
    user_query = get_query_from_sql_file("GetUserDetails")
    params = {
        "username": username
    }
    user_record = FetchOneInDB(query=user_query, params=params)
    if user_record:
        user_id = user_record["user_id"]
        username = user_record["username"]
        hashed_password = user_record["hashed_password"]
        organization_id = user_record.get("organization_id", "")
        if not pwd_context.verify(password, hashed_password):
            return {"is_authorized": False}
        access_token = create_access_token({"user_id": user_id, "organization_id": organization_id})
        return {"access_token": access_token, "token_type": "bearer", "is_authorized": True}
    else:
        return {"is_authorized": False}

