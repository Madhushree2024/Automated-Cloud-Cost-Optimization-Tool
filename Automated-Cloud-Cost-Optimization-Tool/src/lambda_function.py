import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    sns = boto3.client('sns')
    
    # CORRECTED ARN (Removed the subscription ID suffix)
    SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:069062667451:CloudCleanupAlerts"
    
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

    # 3. Send SNS Notification
    if deleted_resources:
        message = "The following unused resources were removed to save costs:\n\n" + "\n".join(deleted_resources)
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="AWS Cleanup Alert",
            Message=message
        )
        print(f"Cleanup successful. Email sent: {deleted_resources}")
        return {"status": "Cleaned", "resources": deleted_resources}
    else:
        print("No unused resources found. No email sent.")
        return {"status": "Success", "message": "No waste found."}
