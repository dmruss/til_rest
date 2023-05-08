from fastapi import APIRouter
import boto3
from pydantic import BaseModel
import datetime
import os
import uuid
from typing import Union

TABLE_NAME = os.environ['FACTS_TABLE_NAME']

class Fact(BaseModel):
    text: str
    tags: Union[str, None] = None

class FactQuery(BaseModel):
    text: Union[str, None] = None
    tags: Union[str, None] = None

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
        if fact.tags:
            tags = fact.tags.split(',')
            tags = str(tags).replace('[', '').replace(']', '').replace("'", '')
        else:
            tags = ''
        response = ddb.put_item(TableName=TABLE_NAME,
            Item={
            'id': {'S': str(uuid.uuid4())},
            'text':{'S':fact.text},
            'date': {'N': str(int(datetime.datetime.timestamp(datetime.datetime.now())))},
            'tags': {'S': tags}
            })
        return 'Success'
    except Exception as e:
        return (str(e))
    
# TODO add search function using a full table scan with filters for each tag and for a text substring
@router.post("/search")
async def search_facts(fact_query: FactQuery):
    tag_list = fact_query.tags.split(',')
    ddb = boto3.client('dynamodb')
    response = ddb.scan(
        TableName=os.environ['FACTS_TABLE_NAME'],
        ExpressionAttributeValues={
            ":tag": {"S": tag_list[0]}
        },
        FilterExpression="contains(tags, :tag)"
    )
    return response
    
    
