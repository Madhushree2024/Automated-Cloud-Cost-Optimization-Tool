import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name='us-east-1')
    sns = boto3.client('sns', region_name='us-east-1')
    
    # Use the ARN from your error log
    SNS_TOPIC_ARN = "yours sns_topic_arn"
    
    deleted_resources = []

    # 1. Clean EBS Volumes
    volumes = ec2.describe_volumes(Filters=[{'Name': 'status', 'Values': ['available']}])
    for vol in volumes['Volumes']:
        v_id = vol['VolumeId']
        ec2.delete_volume(VolumeId=v_id)
        deleted_resources.append(f"Deleted EBS Volume: {v_id}")

    # 2. Clean Elastic IPs
    eips = ec2.describe_addresses()
    for ip in eips['Addresses']:
        if 'InstanceId' not in ip:
            alloc_id = ip['AllocationId']
            public_ip = ip['PublicIp']
            ec2.release_address(AllocationId=alloc_id)
            deleted_resources.append(f"Released Elastic IP: {public_ip}")

    # 3. Send Notification
    if deleted_resources:
        message = "Cost Optimization Report:\n\n" + "\n".join(deleted_resources)
        sns.publish(TopicArn=SNS_TOPIC_ARN, Subject="AWS Cleanup Alert", Message=message)
        return {"status": "Success", "deleted": deleted_resources}
    
    return {"status": "Success", "message": "No waste found."}

