from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda,
    aws_s3,
    aws_lambda_python_alpha
    # aws_sqs as sqs,
)
from constructs import Construct
from os import path


class TilRestStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "TilRestQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
        # bucket = aws_s3.Bucket(self, "til_rest", versioned=True)

        fn = aws_lambda_python_alpha.PythonFunction(self, 
            "til_rest_lambda",
            entry="./src",
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            index="main.py",
            handler="handler"
        )
