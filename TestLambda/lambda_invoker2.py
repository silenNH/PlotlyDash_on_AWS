#https://github.com/awsdocs/aws-doc-sdk-examples/blob/main/python/example_code/lambda/lambda_basics.py

import io
import json
import logging
import zipfile
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)
class LambdaWrapper:
    def __init__(self, lambda_client, iam_resource):
        self.lambda_client = lambda_client
        self.iam_resource = iam_resource


    def invoke_function(self, function_name, function_params, get_log=False):
        """
        Invokes a Lambda function.

        :param function_name: The name of the function to invoke.
        :param function_params: The parameters of the function as a dict. This dict
                                is serialized to JSON before it is sent to Lambda.
        :param get_log: When true, the last 4 KB of the execution log are included in
                        the response.
        :return: The response from the function invocation.
        """
        try:
            response = self.lambda_client.invoke(
                FunctionName=function_name,
                Payload=json.dumps(function_params),
                LogType="Tail" if get_log else "None",
            )
            logger.info("Invoked function %s.", function_name)
        except ClientError:
            logger.exception("Couldn't invoke function %s.", function_name)
            raise
        return response



if __name__== "__main__":
    
    invoker=LambdaWrapper(boto3.client("lambda"), boto3.resource("iam"))
    invoker.invoke_function("map-test-lambda", "{}")