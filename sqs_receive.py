import boto3
from pprint import pprint
import pathlib
import os
import base64,json

def upload_file_to_sqs_using_send_message():
    sqs = boto3.client("sqs", aws_access_key_id='AKIA52M3AL3AZ3O222CR', aws_secret_access_key='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', region_name='us-east-1');
    queue_url = 'https://sqs.us-east-1.amazonaws.com/950049726145/image_request_queue_charan';

    with open("/home/ubuntu/test_4.JPEG", "rb") as image2string:
        converted_string = base64.b64encode(image2string.read())

    message = str(converted_string);

    # Send message to SQS queue
    response = sqs.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=1,
                WaitTimeSeconds=10)

    print(f"Number of messages received: {len(response.get('Messages', []))}")

    for message in response.get("Messages", []):
        message_body = message["Body"]
        print(f"Message body: {json.loads(message_body)}")
        print(f"Receipt Handle: {message['ReceiptHandle']}")


        
    print(response)

upload_file_to_sqs_using_send_message()