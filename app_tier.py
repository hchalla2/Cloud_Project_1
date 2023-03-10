import boto3
from pprint import pprint
import pathlib
import os, subprocess,json,base64
from image_classification import classify_image;
from config import *;
from s3_util import *;
from sqs_util import *;

tmp_folder = "/home/ubuntu/Cloud_Project_1/tmp/";

"""
    This function deletes file from disk of app instance.
"""
def remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

"""
    This function saves file to the disk of app instance.
"""
def save_file(file_path, file_content):
    image_file = open(file_path, 'wb');
    image_file.write(file_content)
    image_file.close();

while True:

    response = receive_message(get_request_queue_url())

    for message in response.get("Messages", []):
        message_body = message["Body"]
        message_dict = json.loads(message_body);
        filename = message_dict['file_name'];
        file_contents = message_dict['file_content'];
        file_name_without_format = filename.split('.')[0] + ".txt";

        delete_message(get_request_queue_url(), message['ReceiptHandle']);

        image_file_path = tmp_folder + filename
        save_file(image_file_path, base64.b64decode(bytes(file_contents, 'utf-8')))

        output = classify_image(image_file_path);

        send_message(get_response_queue_url(), output)

        output_file_path = tmp_folder + "output_" + file_name_without_format;
        save_file(output_file_path, bytes(output, 'utf-8'));

        store_file(get_output_bucket(), output_file_path, "output_" + file_name_without_format);
        store_file(get_input_bucket(), image_file_path, filename);

        remove_file(output_file_path);
        remove_file(image_file_path);




