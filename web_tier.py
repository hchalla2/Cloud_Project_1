from fastapi import FastAPI, UploadFile
import json,base64;
import threading
import asyncio
from config import *;
from sqs_util import *;

app = FastAPI()
lock = threading.Lock()
filename_output_map = {};

def convert_image_to_string(file):
    file_content = file.file.read();
    converted_string = base64.b64encode(file_content)   
    return str(converted_string, 'utf-8');

"""
    This function continuously listens to the queue and updates the global data structure upon receiving the messages 
"""
def queue_listener():
    while True:
        response = receive_message(get_response_queue_url())
        for message in response.get("Messages", []):
            message_body = message["Body"]
            file_output = message_body.split(','); 
            file_name = file_output[0];
            output = file_output[1];

            lock.acquire()
            try:                   
                filename_output_map[file_name] = output;
            finally:
                lock.release();

            delete_message(get_response_queue_url(), message['ReceiptHandle']);

"""
    This function continuously checks the global data structure and returns the output if its populated in the data structure 
"""
async def fetch_output(file_name):
    while True:
        await asyncio.sleep(1);
        with lock:
            if file_name in filename_output_map:
                output = filename_output_map[file_name];
                del filename_output_map[file_name];
                return output;
            else:
                pass;

@app.post("/recognize_image/")
async def recognize_image(myfile: UploadFile):
    file_name = str(myfile.filename);
    file_content = convert_image_to_string(myfile);

    message = {'file_name' : file_name, 'file_content' : file_content};
    body = json.dumps(message);

    # Send message to SQS queue
    send_message(get_request_queue_url(), body);
    
    print("Sent " + file_name + " into the request queue");
    out = await fetch_output(file_name);
    print("Response received:- for " + file_name + "  :- " + out);
    return {file_name : out };


try:
    thread = threading.Thread(target = queue_listener, args = ())
    thread.start();
except:
    print("Error: unable to start queue listener thread")


