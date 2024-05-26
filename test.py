import boto3
import os

session=boto3.Session(aws_access_key_id = os.environ["AWS_ACCESS_KEY"], aws_secret_access_key = os.environ["AWS_SECRET_ACCESS_KEY"], region_name = os.environ["REGION_NAME"])

s3 = session.resource('s3')
my_bucket = s3.Bucket('map-plotly-dash')

for my_bucket_object in my_bucket.objects.all():
    print(my_bucket_object.key)