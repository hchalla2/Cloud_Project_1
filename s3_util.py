import boto3
from config import *;

s3 = boto3.resource("s3", aws_access_key_id=get_access_key(), aws_secret_access_key=get_secret_key())

def store_file(bucket_name, file_path, object_name):
        s3.meta.client.upload_file(file_path, bucket_name, object_name)
