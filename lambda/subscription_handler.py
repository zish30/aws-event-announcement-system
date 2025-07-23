import json
import boto3

sns_client = boto3.client('sns')
SNS_TOPIC_ARN = "arn:aws:sns:ap-south-1:208947927994:event-notifications"

def lambda_handler(event, context):
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS,POST",
        "Access-Control-Allow-Headers": "Content-Type"
    }

    try:
        # Handle preflight OPTIONS request
        if event.get("httpMethod") == "OPTIONS":
            return {"statusCode": 200, "headers": headers, "body": json.dumps({"message": "CORS OK"})}

        body = json.loads(event['body'])
        email = body.get('email')

        if not email:
            return {
                "statusCode": 400,
                "headers": headers,
                "body": json.dumps({"error": "Email is required"})
            }

        sns_client.subscribe(
            TopicArn=SNS_TOPIC_ARN,
            Protocol='email',
            Endpoint=email
        )

        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({"message": f"Subscription request sent to {email}. Please confirm your email."})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"error": str(e)})
        }
