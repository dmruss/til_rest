import aws_cdk as core
import aws_cdk.assertions as assertions

from til_rest.til_rest_stack import TilRestStack

# example tests. To run these tests, uncomment this file along with the example
# resource in til_rest/til_rest_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = TilRestStack(app, "til-rest")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
