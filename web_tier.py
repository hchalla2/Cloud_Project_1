import uvicorn
from fastapi import FastAPI, UploadFile
import json,base64;
import threading,boto3;
import asyncio
import time;

lock = threading.Lock()
app = FastAPI()

result_dict = {};

@app.get("/")
async def root():
    return {"message": "Hello World"}

sqs = boto3.client("sqs", aws_access_key_id='AKIA52M3AL3AZ3O222CR', aws_secret_access_key='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', region_name='us-east-1');
request_queue_url = 'https://sqs.us-east-1.amazonaws.com/950049726145/request_queue_hsh';
response_queue_url = 'https://sqs.us-east-1.amazonaws.com/950049726145/response_queue_hsh';

def queue_listener():
    while True:
        response = sqs.receive_message(QueueUrl=response_queue_url,
                                MaxNumberOfMessages=1,
                                WaitTimeSeconds=10)
        for message in response.get("Messages", []):
            message_body = message["Body"]
            file_output = message_body.split(','); 
            file_name = file_output[0];
            output = file_output[1];

            lock.acquire()
            try:                   
                result_dict[file_name] = output;
            finally:
                lock.release();

            sqs.delete_message(QueueUrl=response_queue_url, ReceiptHandle=message['ReceiptHandle']);

async def get_output(file_name):
    while True:
        with lock:
            if file_name in result_dict:
                output = result_dict[file_name];
                del result_dict[file_name];
                return output;
            else:
                pass;

@app.post("/recognize_image/")
async def recognize_image(file: UploadFile):
    file_name = str(file.filename);
    file_content = file.file.read();
    converted_string = base64.b64encode(file_content)   

    message = {'file_name' : file_name, 'file_content' : str(converted_string, 'utf-8')};
    body = json.dumps(message);

    # Send message to SQS queue
    sqs.send_message(QueueUrl=request_queue_url,
                DelaySeconds=10,
                MessageBody=body)

    out = await get_output(file_name);
    print("Response received:- for file_name " + out);
    return {file_name : out };


try:
    thread = threading.Thread(target = queue_listener, args = ())
    thread.start();
except:
    print("Error: unable to start queue listener thread")


