import boto3
from pprint import pprint
import pathlib
import os

def upload_file_to_sqs_using_send_message():
    sqs = boto3.client("sqs", aws_access_key_id='AKIA52M3AL3AZ3O222CR', aws_secret_access_key='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', region_name='us-east-1');
    queue_url = 'https://sqs.us-east-1.amazonaws.com/950049726145/image_request_queue_charan';

    # Send message to SQS queue
    response = sqs.send_message(
                QueueUrl=queue_url,
                DelaySeconds=10,
                MessageAttributes={
                    'Title': {
                        'DataType': 'String',
                        'StringValue': 'The Whistler'
                    },
                    'Author': {
                        'DataType': 'String',
                        'StringValue': 'John Grisham'
                    },
                    'WeeksOn': {
                        'DataType': 'Number',
                        'StringValue': '6'
                    }    
                },
                MessageBody=(
                    'Information about current NY Times fiction bestseller for '
                    'week of 12/11/2016'
            )
        )
    print(
        response
    )

upload_file_to_sqs_using_send_message();
                                                      