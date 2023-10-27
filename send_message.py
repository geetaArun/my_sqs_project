Import sys
import boto3
Sqs = boto3.client(‘sqs’)
queue_url = ‘https://sqs.us-east-1.amazonaws.com/693512853512/my_demo_sqs’
Response = sqs.send_message (QueueUrl=queue_url, MessageBody=(sys.argv[1]) )
Print(response[‘messageID’])

#Run:
#Python3 send_message.py Peter,USA
#Python3 send_message.py Geeta,India
#Python3 send_message.py John,UK

