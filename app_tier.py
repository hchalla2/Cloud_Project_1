import boto3
from pprint import pprint
import pathlib
import os, subprocess,json,base64
from s3_util import *

s3 = boto3.resource("s3", aws_access_key_id='AKIA52M3AL3AZ3O222CR', aws_secret_access_key='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')
sqs = boto3.client("sqs", aws_access_key_id='AKIA52M3AL3AZ3O222CR', aws_secret_access_key='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', region_name='us-east-1');
request_queue_url = 'https://sqs.us-east-1.amazonaws.com/950049726145/request_queue_hsh';
response_queue_url = 'https://sqs.us-east-1.amazonaws.com/950049726145/response_queue_hsh';

while True:

    response = sqs.receive_message(QueueUrl=request_queue_url,
                                    MaxNumberOfMessages=1,
                                    WaitTimeSeconds=10)


    for message in response.get("Messages", []):
        print("Message received");
        message_body = message["Body"]
        message_dict = json.loads(message_body);
        filename = message_dict['file_name'];
        file_contents = message_dict['file_content'];

        sqs.delete_message(QueueUrl=request_queue_url, ReceiptHandle=message['ReceiptHandle']);

        image_file_path = "/home/ubuntu/app/" + filename
        image_file = open(image_file_path, 'wb');
        image_file.write(base64.b64decode(bytes(file_contents, 'utf-8')))   
        image_file.close();

        output = subprocess.getoutput('python3 /home/ubuntu/image_classification.py ' + temp_file_path);
        print(output);

        sqs.send_message(QueueUrl=response_queue_url, DelaySeconds=10, MessageBody=output)
        print('Response sent');

        output_file_path = "/home/ubuntu/app/output_" + filename;
        output_file = open(output_file_path, 'wb');
        output_file.write(bytes(output, 'utf-8'));
        output_file.close();    

        bucket_name = "output-bucket-hsh"
        object_name = "output_" + filename
        file_name = output_file_path;
        store_file(bucket_name, file_name, object_name);

        if os.path.exists(output_file_path):
            os.remove(output_file_path)

        if os.path.exists(image_file_path):
            os.remove(image_file_path)











