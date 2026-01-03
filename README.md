# Automated-Cloud-Cost-Optimization-Tool
# AWS Automated Cloud Cost Optimizer

## 📌 Overview
This project is a serverless solution designed to reduce AWS infrastructure costs by automatically identifying and deleting orphaned resources. Using **Python** and the **Boto3 SDK**, the system scans for unused EBS volumes and unassociated Elastic IPs, terminates them, and sends a summary report via email.



## 🚀 Features
* **Automated Cleanup**: Removes EBS volumes in 'available' state and unassociated Elastic IPs.
* **Event-Driven**: Scheduled via **Amazon EventBridge** for hands-free maintenance.
* **Real-time Alerts**: Integrates with **Amazon SNS** to provide instant email audit trails.
* **Infrastructure as Code (IAM)**: Implements secure access policies for cross-service communication.

## 🛠️ Technical Stack
* **Language**: Python 3.12
* **AWS SDK**: Boto3
* **Compute**: AWS Lambda
* **Scheduling**: Amazon EventBridge
* **Messaging**: Amazon SNS
* **Logging**: Amazon CloudWatch

## 📊 Proof of Work (Verified Jan 3, 2026)
This project was successfully tested and validated with the following evidence:
* **Scheduled Execution**: Log streams confirm the automation fired successfully at **10:35 UTC**.
* **Cleanup Success**: Verified the deletion of 1GB test volumes and the release of Elastic IPs.
* **Notification**: Confirmed receipt of "AWS Cleanup Alert" email via SNS.

## 📁 Repository Structure
* `src/lambda_function.py`: Main Python logic.
* `iam/policy.json`: IAM and SNS access policies.
* `docs/screenshots/`: Visual proof of CloudWatch logs and SNS alerts.

## 📝 How to Use
1. Deploy the Lambda function with the provided Python script.
2. Attach the required IAM permissions for EC2 and SNS.
3. Configure an SNS Topic and subscribe your email address.
4. Set an EventBridge cron schedule to trigger the function.
