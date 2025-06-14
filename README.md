# AWS Lambda EC2 Management

This project contains an AWS Lambda function that automatically starts and stops EC2 instances based on assigned tags using Python (Boto3).

## ✅ Tags Logic
- Instances tagged with `Action = Auto-Start` → will be **started**
- Instances tagged with `Action = Auto-Stop` → will be **stopped**

## 📂 Files
- `lambda_function.py`: Main Lambda code
- `assignment_1_report.docx`: Assignment documentation with setup and results

## 🧰 Technologies Used
- AWS Lambda
- EC2
- IAM
- Boto3 (Python SDK)

- Screenshots and steps to perform:

- 1. EC2 Setup
1.	Go to EC2 Dashboard → Launch Instance.
2.	Create two t2.micro instances:
o	Use Amazon Linux 2 AMI (free tier).
o	Name them AutoStopInstance and AutoStartInstance for clarity.
3.	Tag them:
o	First instance: Key = Action, Value = Auto-Stop
o	Second instance: Key = Action, Value = Auto-Start

AutoStartInstance
 
 

 

 

 
AutoStopInstance:
 

 
 
 

Both the instances are now running.
 

Confirm Tags and Status
1.	Go to EC2 Dashboard → Instances.
2.	Make sure you see:
o	 AutoStartInstance is running and has tags:
	Name = AutoStartInstance
                                        Action = Auto-Start                               
o	AutoStopInstance is running and has tags:
	Name = AutoStopInstance
	Action = Auto-Stop
 


2. IAM Role Creation for Lambda
2.1: Go to IAM Console
1.	In the sidebar, click Roles and Click the Create role button
 

________________________________________


2.2: Select Trusted Entity
1.	Choose Trusted entity type as: AWS service
2.	Choose Use case: Select Lambda
3.	Click Next
 

________________________________________
2.3: Attach Permissions Policy
	1 In the search box, type: AmazonEC2FullAccess
	2 Check the box next to AmazonEC2FullAccess
	3 Click Next
 
2.4: Name and Create Role:
1.	Role name: LambdaEC2ManagementRole
2.	 Add a description: Role to allow Lambda to start/stop EC2 instances based on tags
3.	Click Create role
 
 

 

Verify the Role:
After creating:
1.	You’ll be taken to the role's summary page.
2.	Under Permissions, you should see: AmazonEC2FullAccess
3.	Under Trusted entities, you should see: Service: lambda.amazonaws.com
  

 

Step 3: Create the Lambda Function to Start/Stop EC2 Instances:
This Lambda function will:
•	Start EC2 instances with tag Action = Auto-Start
•	Stop EC2 instances with tag Action = Auto-Stop
3.1: Go to AWS Lambda Console
1.	Open https://console.aws.amazon.com/lambda
2.	Click Create function
 

3.2: Configure Function:
Field	Value
Function name	ManageEC2InstancesByTag
Runtime	Python 3.12 (or 3.10 / 3.9)
Execution role	Use an existing role
Existing role	LambdaEC2ManagementRole (select the role you created)

Click Create function

 

 

 








3.3: Add the Code
1.	Scroll down to the Code source editor
2.	Replace the default code with this:
3.	import boto3
4.	
5.	def lambda_handler(event, context):
6.	    ec2 = boto3.client('ec2', region_name='ap-south-1')
7.	
8.	    # Get all instances
9.	    instances = ec2.describe_instances()
10.	
11.	    auto_start_ids = []
12.	    auto_stop_ids = []
13.	
14.	    for reservation in instances['Reservations']:
15.	        for instance in reservation['Instances']:
16.	            tags = {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
17.	            instance_id = instance['InstanceId']
18.	
19.	            if tags.get('Action') == 'Auto-Start':
20.	                ec2.start_instances(InstanceIds=[instance_id])
21.	                auto_start_ids.append(instance_id)
22.	
23.	            elif tags.get('Action') == 'Auto-Stop':
24.	                ec2.stop_instances(InstanceIds=[instance_id])
25.	                auto_stop_ids.append(instance_id)
26.	
27.	    return {
28.	        'statusCode': 200,
29.	        'body': {
30.	            'message': 'EC2 instances managed successfully',
31.	            'started_instances': auto_start_ids,
32.	            'stopped_instances': auto_stop_ids
33.	        }
34.	    }
35.	

Click Deploy after pasting the code.
 

 
3.4: Test the Lambda Function
Click the Test tab (next to Code).
Configure a test event:
•	Event name: TestEC2StartStop
•	Event sharing setting: Private
•	Leave the default JSON as-is:
{}
Click Save and Test
 
 

 


What to Expect:
•	If AutoStartInstance was stopped → it will start
•	If AutoStopInstance was running → it will stop
•	Logs will show which instances were started/stopped
Go to EC2 → Instances and verify the state changes. This may take 30–60 seconds



If you see error message:
"errorType": "Sandbox.Timedout",
"errorMessage": "Task timed out after 3.00 seconds"
 
means your Lambda function exceeded the default timeout, which is 3 seconds — this is common when starting/stopping EC2 instances, as these actions take a few seconds.
Fix: Increase the Lambda Timeout:
Step-by-Step:
1.	Go to your Lambda function in the AWS console
https://console.aws.amazon.com/lambda
2.	On the left, click Configuration
3.	Then click General configuration
4.	Click Edit
5.	Under Timeout, change it from 3 seconds to 30 seconds (or even 1 minute if you'd like extra buffer)
6.	Click Save
Now Try Again
After updating the timeout:
•	Go to the Test tab
•	Click Test again


You should now see a success response like:
{
  "statusCode": 200,
  "body": "EC2 instances managed successfully"
}
And in the logs:
Started instances: ['i-xxxxxxx']
Stopped instances: ['i-yyyyyyy']

 

 
 

Currently both the instances are stopped and now let’s run the test in Lambda.
 

After clicking TEST:
 

 
 
 
 

This output means your Lambda function executed successfully and managed your EC2 instances as intended.
Response body:
{
  "statusCode": 200,
  "body": {
    "message": "EC2 instances managed successfully",
    "started_instances": [
      "i-02b7e6df027207099",
      "i-096241e049ee9706b",
      "i-05b08e99e20bbbe8f",
      "i-0d8447825904afe47"
    ],
    "stopped_instances": [
      "i-009ba400913499d82",
      "i-0d2f789be215b0abc",
      "i-051974c4ee5f05600",
      "i-02867c2861fd919e8",
      "i-05fa521ebdb762689"
    ]
  }
}



"message": "EC2 instances managed successfully" — confirms the function completed without errors.
"started_instances": ["i-02b7e6df027207099"] — this instance (tagged Auto-Start) was started by the Lambda function.
"stopped_instances": ["i-009ba400913499d82"] — this instance (tagged Auto-Stop) was stopped by the Lambda function.

Logs:
START RequestId: 0a57afe9-7f93-4da0-b313-08f1ac5a280d Version: $LATEST
END RequestId: 0a57afe9-7f93-4da0-b313-08f1ac5a280d
REPORT RequestId: 0a57afe9-7f93-4da0-b313-08f1ac5a280d	Duration: 1514.16 ms	Billed Duration: 1515 ms	Memory Size: 128 MB	Max Memory Used: 95 MB

START and END mark the start and finish of your Lambda execution.
REPORT shows how long the function ran (about 1.5 seconds), the memory used, and billing info.

Summary:
Lambda function detected that:
•	The instance tagged for Auto-Start was stopped, so it started it.
•	The instance tagged for Auto-Stop was running, so it stopped it.
Everything ran smoothly without errors.


## 📌 Author
Vignesh Sadanki
