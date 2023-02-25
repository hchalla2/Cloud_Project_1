import pathlib
import os

def upload_file_to_s3_using_put_object():
    """
    Uploads file to s3 using put_object function of resource object.
    Same function is available for s3 client object as well.
    put_object function gives us much more options and we can set object access policy, tags, encryption etc
    :return: None
    """
    s3 = boto3.resource("s3", aws_access_key_id='AKIA52M3AL3AZ3O222CR', aws_secret_access_key='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')
    bucket_name = "test-first-charan"
    object_name = "image_classification.py"
    file_name = "image_classification.py"
    bucket = s3.Bucket(bucket_name)
    response = bucket.put_object(
        ACL="private",
        Body=file_name,
        ServerSideEncryption="AES256",
        Key=object_name,
        Metadata={"env": "dev", "owner": "binary guy"},
    )
    print(
        response
    )  # prints s3.Object(bucket_name='binary-guy-frompython-2', key='sample_using_put_object.txt')

upload_file_to_s3_using_put_object();