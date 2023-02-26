import boto3;
import config;

sqs = boto3.client("sqs", aws_access_key_id=get_access_key(), aws_secret_access_key=get_secret_key(), region_name='us-east-1');

def send_message(queue_url, body):
    sqs.send_message(QueueUrl=queue_url, DelaySeconds=10, MessageBody=body)
    return 0;

def delete_message(queue_url, recipient_handle):
    sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=recipient_handle);
    return 0;

def receive_message(queue_url):
    response = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=1, WaitTimeSeconds=10)
    return response;


