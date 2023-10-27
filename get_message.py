Import time
Import sys
import mysql.connector

queue_url = 'https://sqs.us-east-1.amazonaws.com/693512853512/my_demo_sqs'

#Specify the database details
host = 'demo-rds.c12m8e5qyjms.us-east-1.rds.amazonaws.com'

user = 'rdsuser'
password = 'write the configured pass'
database='demo'

#Create a SQS Client
sqs = boto3.client('sqs')

#Connect to the RDS MySQL Instance
mydb = mysql.connector.connect(host=host, user=user, password=password, database=database)
mycursor = mydb.cursor()

# Receive message from SQS queue
response = sqs.receive_message(QueueUrl=queue_url)
message = response['Messages'][0]

# Delete received message from queue
receipt_handle = message['ReceiptHandle']
sqs.delete_message(
QueueUrl=queue_url,
ReceiptHandle=receipt_handle
)
print('Received and deleted message: %s' % message["Body"])

#Get the customer name and address from the message

customerDetails = message["Body"]
customerDetailsList = customerDetails.split(',')
name = customerDetailsList[0]
address = customerDetailsList[1]

#Write the record to the database

val = (name, address)
sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"

mycursor.execute(sql, val)
mydb.commit()

print("Record inserted in the DB")


#Run this script:
#Python3 getmessage.py

#Select * from customers: to check if db entries are inserted 
#Check console sqs to see messages are read and deleted.
