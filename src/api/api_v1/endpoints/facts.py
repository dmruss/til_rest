from fastapi import APIRouter
import boto3
from pydantic import BaseModel
import datetime
import os
import uuid

TABLE_NAME = os.environ['FACTS_TABLE_NAME']

class Fact(BaseModel):
    text: str

router = APIRouter()

@router.get("/")
async def get_facts():
    
    ddb = boto3.client('dynamodb')
    response = ddb.scan(
        TableName=os.environ['FACTS_TABLE_NAME']
    )
    return response

@router.post("/")
async def post_fact(fact: Fact):
    ddb = boto3.client('dynamodb')
    try:

        response = ddb.put_item(TableName=TABLE_NAME,
            Item={
            'id': {'S': uuid.uuid4()},
            'text':{'S':fact.text},
            'date': {'S': datetime.datetime.now().strftime('%D') }
            })
        return 'Success'
    except Exception as e:
        return (str(e))
    
    
