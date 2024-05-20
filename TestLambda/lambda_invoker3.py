#https://gist.github.com/GabrielSGoncalves/5668b1172d44620b759998534baa9026

import boto3
import json
import sys

#BUCKET = sys.argv[1]
#KEY = sys.argv[2]
#OUTPUT = sys.argv[3]
#GROUP = sys.argv[4]
#COLUMN = sys.argv[5]
#CREDENTIALS = sys.argv[6]

# Use credentials from JSON file
#try:
#    with open(CREDENTIALS) as json_file:
#        credentials_json = json.load(json_file)
#    assert credentials_json['access_key_id'], "Did not find 'access_key_id'"
#    assert credentials_json['secret_access_key'], "Did not find 'secret_access_key'"
#except:
#    print('Error related to JSON Credentials')
#    sys.exit()


def invoke_lambda(bucket, file_key):
    """Invoke Lambda function using boto3
    Parameters:
    - bucket: Name of your S3 bucket
    - file_key: Name of your CSV file on the S3 bucket
    - output_file: Name for the output CSV file
    - group: Column to use as group in groupby
    - column: Column to aggregate in groupby
    """
    #global credentials_json
    
    # Set Lambda Client with credentials
    #boto3.setup_default_session(region_name='us-east-1')
    client = boto3.client('lambda')
    #    'lambda',
    #    aws_access_key_id=credentials_json.get('access_key_id'),
    #    aws_secret_access_key=credentials_json.get('secret_access_key')
    #)

    # Dictionary to be posted on the lambda event with information provided
    # by the user command line call
    payload = {
        "bucket": bucket,
        "file_key": file_key,
        #"output_file": output_file,
        #"group": group,
        #"column": column
    }

    response = client.invoke(
        FunctionName='map-test-lambda',
        InvocationType='RequestResponse',
        LogType='Tail',
        Payload=json.dumps(payload)
    )
    return response

print(invoke_lambda("map-plotly-dash", "20211011_103504.jpg")['Payload'].read())