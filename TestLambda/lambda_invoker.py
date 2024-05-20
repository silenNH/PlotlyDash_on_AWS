#https://www.youtube.com/watch?v=RAty97aORKA
import boto3
import configparser
import json
import time

class lambda_sample:
    def __init__(self, lambda_name, role_name, policy_name):
        self.lambda_name = lambda_name
        self.role_name =role_name
        self.policy_name = policy_name
    
    def aws_create_role(self):
        client=session.client("iam")
        trust_doc=json.load(open("trust_relationship.json"))
        role_create= client.create_role(
            RoleName= self.role_name,
            AssumeRolePolicyDocument = json.dumps(trust_doc),
            Description = "IAM role to manage Lambda",
            Tags= [
                {
                    "Key":"Name", 
                    "Value":self.role_name
                },
                {
                    "Key":"Category", 
                    "Value":"Demo"   
                }
                ]
            )
        return role_create["Role"]["Arn"]
    
    def aws_create_policy(self):
        client=session.client("iam")
        policy_doc=json.load(open("policy_doc.json"))
        policy_create=client.create_policy(
            PolicyName=self.policy_name,
            PolicyDocument=json.dumps(policy_doc),
            Description= "IAM Policy to manage lambda",
            Tags= [
                {
                    "Key":"Name", 
                    "Value":self.policy_name
                },
                {
                    "Key":"Category", 
                    "Value":"Demo"   
                }
                ]
            )
        return policy_create["Policy"]["Arn"]
        
    def aws_attach_policy(self, policy_arn):
        client = session.client("iam")
        policy_attach = client.attach_role_policy(
            RoleName=self.role_name,
            PolicyArn=policy_arn
            )
        return policy_attach["ResponseMetadata"]["HTTPStatusCode"]
        
    
    def create_lambda(self, role_arn):
        lambda_session =session.client("lambda")
        func = lambda_session.create_function(
            FunctionName=self.lambda_name,
            Runtime="python3.9",
            Handler="lambda_function.lambda_handler",
            Role = role_arn,
            Description = "AWS Lambda to List S3 Objects",
            Timeout =30,
            MemorySize =200,
            Tags = {
                "Name":"S3 Test Lambda",
                "Category": "Demo"
            },
            Code= {
                "S3Bucket": "silen-lambda-test",
                "S3Key" :"lambda_test.zip"
            }
            )
        return func["FunctionArn"]
    
    def invoke_lambda(self,lambda_arn):
        client = session.client("lambda")
        func = client.invoke(
            FunctionName = lambda_arn,
            InvocationType = "RequestResponse"
            )
        return func["Payload"]
         
if __name__== "__main__":
    secretparser=configparser.ConfigParser()
    secretparser.read('confi.ini')
    session=boto3.session(
        aws_access_key_id=secretparser["AWS_Secrets"]["aws_access_key_id"],
        aws_secret_access_key=secretparser["AWS_Secrets"]["aws_secret_access_key"],
        region_name=secretparser["AWS_SECRETS"]["AWS_Region"]
        )
    
    training = lambda_sample("lambda_test", "lambda_demo_role", "lampda_demo_policy")
    r_arn = training.aws_create_role()
    print(r_arn)
    p_arn=training.aws_create_policy()
    print(p_arn)
    print( training.aws_attach_policy(policy_arn=p_arn))
    time.sleep(10)
    l_arn=training.create_lambda(role_arn=r_arn)
    print(l_arn)
    invoke_status = training.invoke_lambda(lambda_arn=l_arn)
    print(invoke_status.read())