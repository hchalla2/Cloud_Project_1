import boto3
from pprint import pprint
import pathlib
import os, subprocess,json,base64
from s3_util import *
from image_classification import classify_image;
from config import *;


s3 = boto3.resource("s3", aws_access_key_id=get_access_key(), aws_secret_access_key=get_secret_key())
sqs = boto3.client("sqs", aws_access_key_id=get_access_key(), aws_secret_access_key=get_secret_key(), region_name='us-east-1');
tmp_folder = "/home/ubuntu/Cloud_Project_1/tmp/";

def remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

def save_file(file_path, file_content):
    image_file = open(file_path, 'wb');
    image_file.write(file_content)
    image_file.close();

while True:

    response = sqs.receive_message(QueueUrl=get_request_queue_url(),
                                    MaxNumberOfMessages=1,
                                    WaitTimeSeconds=10)


    for message in response.get("Messages", []):
        message_body = message["Body"]
        message_dict = json.loads(message_body);
        filename = message_dict['file_name'];
        file_contents = message_dict['file_content'];

        file_name_without_format = filename.split('.')[0] + ".txt";

        sqs.delete_message(QueueUrl=get_request_queue_url(), ReceiptHandle=message['ReceiptHandle']);

        image_file_path = tmp_folder + filename
        save_file(image_file_path, base64.b64decode(bytes(file_contents, 'utf-8')))

        output = classify_image(image_file_path);
        # print(output);

        sqs.send_message(QueueUrl=get_response_queue_url(), DelaySeconds=10, MessageBody=output)
        # print('Response sent');

        output_file_path = tmp_folder + "output_" + file_name_without_format;
        save_file(output_file_path, bytes(output, 'utf-8'));

        store_file(get_output_bucket(), output_file_path, "output_" + file_name_without_format);
        store_file(get_input_bucket(), image_file_path, filename);

        remove_file(output_file_path);
        remove_file(image_file_path);




