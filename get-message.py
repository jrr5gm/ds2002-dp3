
import boto3
from botocore.exceptions import ClientError
import requests
import json

# Set up your SQS queue URL and boto3 client
url = "https://sqs.us-east-1.amazonaws.com/440848399208/jrr5gm"
sqs = boto3.client('sqs')

def delete_message(handle):
    try:
        # Delete message from SQS queue
        sqs.delete_message(
            QueueUrl=url,
            ReceiptHandle=handle
        )
        print("Message deleted")
    except ClientError as e:
        print(e.response['Error']['Message'])

def get_message():
    try:
        message_pairs = []
        receipt_handles = []
        for _ in range(10):
            # Receive message from SQS queue. Each message has two MessageAttributes: order and word
            # You want to extract these two attributes to reassemble the message
            response = sqs.receive_message(
                QueueUrl=url,
                AttributeNames=[
                    'All'
                ],
                MaxNumberOfMessages=1,
                MessageAttributeNames=[
                    'All'
                ]
            )
            # Check if there is a message in the queue or not
            if "Messages" in response:
                # extract the two message attributes you want to use as variables
                # extract the handle for deletion later
                message = response['Messages'][0]
                order = response['Messages'][0]['MessageAttributes']['order']['StringValue']
                word = response['Messages'][0]['MessageAttributes']['word']['StringValue']
                handle = response['Messages'][0]['ReceiptHandle']
                message_pairs.append((order,word))
                receipt_handles.append(handle)
        # If there is no message in the queue, print a message and exit    
            else:
                print("No message in the queue")
        
        # Sort messages based on order value 
        message_pairs.sort(key=lambda x: x[0])

        # Assemble words based on order
        assembled_message = ' '.join(word for _, word in message_pairs)

        # Print the message attributes - this is what you want to work with to reassemble the message
        print(assembled_message)

        # Delete messages
        for handle in receipt_handles:
            delete_message(handle)   

    # Handle any errors that may occur connecting to SQS
    except ClientError as e:
        print(e.response['Error']['Message'])

# Trigger the function
if __name__ == "__main__":
    get_message()

