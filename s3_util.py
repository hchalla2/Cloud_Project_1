import boto3

s3 = boto3.resource("s3", aws_access_key_id='AKIA52M3AL3AZ3O222CR', aws_secret_access_key='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')

def store_file(bucket_name, file_path, object_name):
        s3.meta.client.upload_file(file_path, bucket_name, object_name)
