
from dash import  html, dcc, callback, Input, Output, State, no_update
import dash_bootstrap_components as dbc
#import plotly.express as px
import dash
import dash_uploader as du
from boto3 import client
import boto3
import os
import uuid
from datetime import datetime
import logging
import json
from botocore.exceptions import ClientError
import requests 


UPLOAD_FOLDER_ROOT = "/home/ec2-user/environment/uploads" #os.path.join(os.path.dirname(__file__),"uploads")
#Get all Files in the S3 Bucket
upload_bucket_name="map-plotly-dash"
download_bucket_name="silen-lambda-test"

filesUploadBucket=[]
filesInDownloadBucket=[]
listOfFolders=[]
def get_filesinBucket(bucket_name):
    filesInBucket=[]
    conn = client('s3')  # again assumes boto.cfg setup, assume AWS S3
    for key in conn.list_objects(Bucket=bucket_name)['Contents']:
        filesInBucket.append(key['Key'])
        #print(key['Key'])
    return filesInBucket
#get_filesinBucket()
filesUploadBucket=get_filesinBucket(upload_bucket_name)
filesInDownloadBucket=get_filesinBucket(download_bucket_name)
def get_filePathForUploadToS3():
    filePathForUploadToS3=[]
    for root, dirs, files in os.walk(UPLOAD_FOLDER_ROOT, topdown=False):
       for name in files:
          filePathForUploadToS3.append(os.path.join(root, name))
    return filePathForUploadToS3
    
def get_DirectoryPathForUploadToS3():
    listOfFolders=[]
    for root, dirs, files in os.walk(UPLOAD_FOLDER_ROOT, topdown=False):
       for directory in dirs:
          listOfFolders.append(os.path.join(root, directory))
    return listOfFolders
          #print(os.path.join(root, name))
       #for name in dirs:
        #  print(os.path.join(root, name))

def delete_files(file_path):
    os.remove(file_path)
    #print("test")

def delete_directories(dir_path):
    #os.removedirs(os.path.dirname(file_path))    
    os.removedirs(dir_path)
    
def upload_fileToS3(file_name, bucket_name, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    #print(file_name)
    # If S3 object_name was not specified, use file_name
    
    if object_name is None:
        object_name = os.path.basename(file_name)
    #print(object_name)
    #print(file_name)
    #print(bucket_name)
    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket_name, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def invoke_lambda(bucket, file_key):
    """Invoke Lambda function using boto3
    Parameters:
    - bucket: Name of your S3 bucket
    - file_key: Name of your CSV file on the S3 bucket
    """
    
    # Set Lambda Client with credentials
    client = boto3.client('lambda')

    # Dictionary to be posted on the lambda event with information provided
    # by the user command line call
    payload = {
        "bucket": bucket,
        "file_key": file_key,
    }
    response = client.invoke(
        FunctionName='map-test-lambda',
        InvocationType='RequestResponse',
        LogType='Tail',
        Payload=json.dumps(payload)
    )
    return response

#https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-presigned-urls.html
def create_presigned_url(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """
    print(bucket_name)
    print(type(object_name))
    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response
    
    

dash.register_page(__name__)



layout = dbc.Container([
    
    
    dcc.Location(id="ATool"),
    html.H1(children='Allocation Tool/ UpTime-izer'),
    html.Hr(),


    html.H2(children='Upload Section:'),
    html.H4(children="1) Upload your files to the server:"),
    html.Br(),
    du.Upload(
        id='dash-uploader',
        text='Drag and Drop Here to upload!',
        text_completed='Uploaded: ',
        text_disabled='The uploader is disabled.',
        cancel_button=True,
        pause_button=True,
        disabled=False,
        filetypes=['png','jpg', 'csv', 'xlsx'],
        default_style = {
                                                'width': '100%',
                                                'height': '30px',
                                                'lineHeight': '60px',
                                                'borderWidth': '2px',
                                                'borderStyle': 'dashed',
                                                'borderRadius': '5px',
                                                'textAlign': 'center',
                                                'margin': '0px',
                                                'margin-bottom' : '10px',
                                                'color' : 'green'},
        upload_id="AT-"+ str(datetime.now())
        ),
    
    html.Br(),
    html.H4(children="2) Upload your files from the server to the S3 Bucket:"),
    html.Br(),
    dbc.Row([
            dbc.Col([
            dbc.Button("Click to Upload to S3", color="secondary", id='S3UploadButton', className="me-1",n_clicks=0),    
            ])

    ]),
    dbc.Alert("", color="Primary", id="Alert0"),
    html.Br(),
    html.Br(),
    html.Hr(),
    html.H2(children='Define Run Parameters:'), 
    html.Br(),
    html.H4(children="3) Select the input file to be used in execution:"),
    html.Br(),
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                filesUploadBucket,
                 id="S3FileUploadDropDown", 
                clearable=False
                ),
            ]),
        dbc.Col([
            html.H4(children='Please select the S3 file in the given S3 Bucket which should be used during execution'),      
        ], width=6)],
          className='mb-1'),
    
    html.Br(),
    html.Br(),
    html.Hr(),
    html.H2(children='Run on DMC'),
    html.Br(),
    html.H4(children="4) Click the button to execute the script in DMC with the selected input file:"),
    html.Br(),
    dbc.Row([
            dbc.Col([
            dbc.Button("Click to execute on DMC", color="secondary", id='my-button', className="me-1",n_clicks=0),    
            ])

    ]),
    dbc.Row([
    dbc.Alert("", color="Primary", id="Alert1"),
        ]),
    html.Br(),
    html.Hr(),
    html.H2(children='Download Results'), 
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                filesInDownloadBucket,
                 id="S3FileDropDownDownload", 
                clearable=False
                ),
            ]),
        dbc.Col([
            html.H4(children='Please select the S3 result file in the given S3 Bucket for downloading'),      
        ], width=6)],
          className='mb-1'),
    html.Br(),
    html.H4(children="5) Refresh the result drop down:"),
    html.Br(),
    dbc.Row([
        dbc.Button("Refresh the Dropdown", color="secondary", id='refresh-button', className="me-1",n_clicks=0),    
            ]),
    html.Br(),
    html.H4(children="6) Chose the corresponding result file in the dropdown and press the download button to generate an presigned URL:"),
    html.Br(),
    dbc.Row([
        dbc.Button("Click to download the choosen result file", color="secondary", id='download-button', className="me-1",n_clicks=0),    
        ]),

    html.Br(),
    dbc.Row([
        dbc.Col([
            html.H4(children='The presigned URL link is:')
        ]),
        dbc.Col([
            dbc.Alert("", color="Primary", id="Alert2"),
        ]),
        ]),
    

])

@callback(
    Output(component_id='Alert1', component_property="children"),
    Input(component_id='my-button', component_property='n_clicks'),
    State(component_id='S3FileUploadDropDown', component_property='value'), 
    )
def execute_dmc(button, ChosenFile):

    print("Hello5")
    #invoke_lambda(UPLOAD_FOLDER_ROOT, ChosenFile)
    print(invoke_lambda(UPLOAD_FOLDER_ROOT, ChosenFile)['Payload'].read())
    return ChosenFile   


@callback(
    Output('S3FileDropDownDownload', 'options'),
    Input(component_id='refresh-button', component_property='n_clicks'))
    
def refresh_DownloadDropdown(n_clicks):
    filesInDownloadBucket=[]
    filesInDownloadBucket=get_filesinBucket(download_bucket_name)
    return filesInDownloadBucket
    
    
@callback(
    Output('Alert2', 'children'), 
    Input(component_id='download-button', component_property='n_clicks'),
    State('S3FileDropDownDownload', 'value'),
    prevent_initial_call=True)
def download_result(n_clicks, value):
    #print(type(download_bucket_name))
    #print(type(value))
    url = create_presigned_url(download_bucket_name, value, expiration=3600)
    #if url is not None:
        #response = requests.get(url)
        #print(response)
    return str(url)

@callback(
    Output(component_id='S3FileUploadDropDown', component_property='options'), 
    Input(component_id='S3UploadButton', component_property='n_clicks'))
def S3UploadCallback(n_clicks):
    
    
    filePathForUploadToS3=get_filePathForUploadToS3()
    print("Test123")
    print(filePathForUploadToS3)
    for file in filePathForUploadToS3:
        print("test456")
        print(file)
        upload_fileToS3(file,upload_bucket_name)
        delete_files(file)
    
    listOfFolders=get_DirectoryPathForUploadToS3()
    print(listOfFolders)
    for directory in listOfFolders:
        print("test789")
        print(directory)
        delete_directories(directory)
    filesUploadBucket=[]
    filesUploadBucket=get_filesinBucket(upload_bucket_name)
    #print(filesUploadBucket)
    return filesUploadBucket

    
    