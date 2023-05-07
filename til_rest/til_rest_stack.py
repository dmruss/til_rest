from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda,
    aws_lambda_python_alpha,
    aws_dynamodb,
    aws_apigateway
)
from constructs import Construct
from os import path


class TilRestStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        
        table = aws_dynamodb.Table(self, "til_rest_table",
            partition_key=aws_dynamodb.Attribute(name="id", type=aws_dynamodb.AttributeType.STRING)
        )

        fn = aws_lambda_python_alpha.PythonFunction(self, 
            "til_rest_lambda",
            entry="./src",
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            index="main.py",
            handler="handler",
            environment= {
                'FACTS_TABLE_NAME': table.table_name
            }
            
        )

        table.grant_read_data(fn)

        method_options = aws_apigateway.MethodOptions(api_key_required=True)
        stage_options = aws_apigateway.StageOptions(stage_name='dev')

        api = aws_apigateway.LambdaRestApi(self,
            "til_rest_api",
            handler=fn,
            proxy=True,
            default_method_options=method_options,
            deploy=True,
            deploy_options=stage_options)
        
        usage_plan = api.add_usage_plan('til_rest_usage_plan', name='til_rest_usage_plan')
        usage_plan.add_api_stage(stage=api.deployment_stage)
        key = aws_apigateway.ApiKey(scope=api, id="til_rest_api_key")
        usage_plan.add_api_key(key)
        
       

        
        
        