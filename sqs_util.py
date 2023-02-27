import boto3;
from config import *;

sqs = boto3.client("sqs", aws_access_key_id=get_access_key(), aws_secret_access_key=get_secret_key(), region_name='us-east-1');

def send_message(queue_url, body):
    try:
        sqs.send_message(QueueUrl=queue_url, DelaySeconds=10, MessageBody=body)
    except:
        print("Sending message to queue has failed");

def delete_message(queue_url, recipient_handle):
    try:
        sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=recipient_handle);
    except:
        print("Deleting message in the queue has failed")

def receive_message(queue_url):
    try:
        response = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=1, WaitTimeSeconds=10)
        return response;
    except:
        print("Receive operation from the queue didn't work");

