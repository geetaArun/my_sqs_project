# my_sqs_project

Create sqs queue in AWS : SQS demo queue standard settings
Creas RDS in AWS : mysql Deafult
Create EC2’s in AWS
Write Python scripts to communicate between services
Front end ec2 script : send messages to SQS
Back end ec2 script : reads the message from SQS, Inserts into DB and delete the message from SQS.

Create IAM User
IAM user : user_sqs
Access : AKIA2C6EWLAEIY6DNTFS
Secret : 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

User IAM policies attached:
Sqsfulaccess
Rdsfullaccess
awsAdminaccess (to run python on ec2)

Console : Create SQS queue : my_demo_sqs
SQS URL: https://sqs.us-east-1.amazonaws.com/693512853512/my_demo_sqs
SQL ARN : arn:aws:sqs:us-east-1:693512853512:my_demo_sqs

Console : Create RDS Mysql DB: Standard, do not forget to give allow public access
Create RDS mysql :demo-rds

RDS User Cred:
user as rdsuser,
Password : rdsuserpass
Vpc : vpc-08ddb0a6a344aa85e
Subnet: default

Open AWS cloud shell from rds
Then install mysql cli to connect to DB
So..run 
sudo yum update 
sudo yum install mysql

RDS Endpoint : demo-rds.c12m8e5qyjms.us-east-1.rds.amazonaws.com

Confirm security groups:
The default security group associated with RDS, RDS vpc, update security group as below.
sg-0882d6118056fa838

IB rules:
Custom TCP : port 3306 from anywhere-ipv4  type : Mysql/aurora
3306 from anywhere

On Cloud shell connect to mysql:
mysql -u rdsuser -p -h  demo-rds.c12m8e5qyjms.us-east-1.rds.amazonaws.com

Create database demo;
Use demo;
Create table customers (
Name VARCHAR(30) NOT NULL,
Address VARCHAR(30) NOT NULL
);

Desc customers; (describe customers)
Select * from customers —> 0 rows yet, insert from VM from SQL into RDS mysql demo DB, customers table

Here in this project VM’s are created in Azure, you can even create EC2 in AWS?
Multi cloud way of using resources:
Here VM’s from AWS
All other services from AWS


Ec2, Iam user to ssh to these ec2’s : linux/ubuntu
With ssh private keys : .pem file

Have the scripts to perform all the insert msg to sqs/pull from sqs msg/insert into mysql customers/delete msg from sqs actions.


Frontend EC2:
Install AWS cli

sudo yum update
sudo yum install awscli

Configure was cli :
aws configure
AKIA2C6EWLAEIY6DNTFS
AAx4w1iTTE1CAEsQbmLyiqCQ7dvxNpvZLxb5n7KT
Region : us-east-1
Output format : table (json)

Install python on both VM’s
sudo su  first OR use sudo with apt cmd
sudo yum update
sudo  yum install -y python
yum install python3-pip
pip install boto3

Installl mysql connector on the vm that connects to mysql RDS
pip install mysql-connector-python

Create a script on frontend vm to send the msg to sqs
Connect to frontend VM

Vi send_message.py
Import sys
import boto3
Sqs = boto3.client(‘sqs’)
queue_url = ‘ <sqs url from console>’
Response = sqs.send_message (QueueUrl=queue_url, MessageBody=(sys.argv[1]) )
Print(response[‘messageID’])

Run:
Python3 send_message.py Peter,USA
Python3 send_message.py Geeta, ndia
Python3 send_message.py John, UK

Configure backend ec2 as well:

install AWS cli

sudo yum update
sudo yum install awscli

Configure was cli :
aws configure
AKIA2C6EWLAEIY6DNTFS
AAx4w1iTTE1CAEsQbmLyiqCQ7dvxNpvZLxb5n7KT
Region : us-east-1
Output format : table (json)

Install python on both VM’s
sudo su  first OR use sudo with apt cmd
sudo yum update
sudo  yum install -y python
yum install python3-pip
pip install boto3

Installl mysql connector on the vm that connects to mysql RDS
pip install mysql-connector-python

Create a script on backend to pull from SQS, insert in RDS, delete from SQS
Vi get_message.py
import mysql.connector

queue_url = 'https://sqs.us-east-1.amazonaws.com/693512853512/my_demo_sqs'

#Specify the database details
host = 'demo-rds.c12m8e5qyjms.us-east-1.rds.amazonaws.com'

user = 'rdsuser'
password = 'rdsuserpass'
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


Run this script:
Python3 getmessage.py

Select * from customers: to check if db entries are inserted 
Check console sqs to see messages are read and deleted.

