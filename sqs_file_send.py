import boto3
from pprint import pprint
import pathlib
import os
import json
import base64


def upload_file_to_sqs_using_send_message():
    sqs = boto3.client("sqs", aws_access_key_id='AKIA52M3AL3AZ3O222CR', aws_secret_access_key='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', region_name='us-east-1');
    queue_url = 'https://sqs.us-east-1.amazonaws.com/950049726145/image_request_queue_charan';

    with open("/home/ubuntu/test_4.JPEG", "rb") as image2string:
        converted_string = base64.b64encode(image2string.read())

    message = {'filename' : 'test_4.JPEG', 'content' : str(converted_string, 'utf-8')};
    body = json.dumps(message);
    # Send message to SQS queue
    response = sqs.send_message(
                QueueUrl=queue_url,
                DelaySeconds=10,
                MessageBody=body)

    print(response)

upload_file_to_sqs_using_send_message()

                                                     