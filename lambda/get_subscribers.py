import json
import boto3

sns_client = boto3.client('sns')

SNS_TOPIC_ARN = "arn:aws:sns:ap-south-1:208947927994:event-notifications"

def lambda_handler(event, context):
    try:
        subscribers = []
        next_token = None
        
        while True:
            if next_token:
                response = sns_client.list_subscriptions_by_topic(
                    TopicArn=SNS_TOPIC_ARN,
                    NextToken=next_token
                )
            else:
                response = sns_client.list_subscriptions_by_topic(
                    TopicArn=SNS_TOPIC_ARN
                )
            
            for sub in response.get('Subscriptions', []):
                endpoint = sub.get('Endpoint')
                if endpoint and sub.get('SubscriptionArn') != 'PendingConfirmation':
                    subscribers.append(endpoint)
            
            next_token = response.get('NextToken')
            if not next_token:
                break
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"subscribers": subscribers})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": str(e)})
        }
