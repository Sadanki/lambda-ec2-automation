import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name='ap-south-1')
    auto_start_ids = []
    auto_stop_ids = []

    instances = ec2.describe_instances()

    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            tags = {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
            instance_id = instance['InstanceId']

            if tags.get('Action') == 'Auto-Start':
                ec2.start_instances(InstanceIds=[instance_id])
                auto_start_ids.append(instance_id)
                print(f"Started instance: {instance_id}")

            elif tags.get('Action') == 'Auto-Stop':
                ec2.stop_instances(InstanceIds=[instance_id])
                auto_stop_ids.append(instance_id)
                print(f"Stopped instance: {instance_id}")

    print("Lambda execution complete")

    return {
        'statusCode': 200,
        'body': {
            'message': 'EC2 instances managed successfully',
            'started_instances': auto_start_ids,
            'stopped_instances': auto_stop_ids
        }
    }
