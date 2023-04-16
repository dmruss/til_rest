from fastapi import APIRouter
import boto3
from pydantic import BaseModel

class User(BaseModel):
    username : str

router = APIRouter()

@router.get("/")
async def get_users():
    ddb = boto3.client('dynamodb')
    response = ddb.scan(
        TableName='serverless-fastapi-lambda-dev9'
    )
    return response

@router.post("/")
async def post_user(user: User):
    ddb = boto3.client('dynamodb')
    try:
        response = ddb.put_item(TableName='serverless-fastapi-lambda-dev9',Item={'username':{'S':user.username}})
        return 'Success'
    except Exception as e:
        return (str(e))
    
    
