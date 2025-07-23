import json
import boto3

sns_client = boto3.client('sns')
s3_client = boto3.client('s3')

SNS_TOPIC_ARN = "arn:aws:sns:ap-south-1:208947927994:event-notifications"
BUCKET_NAME = "event-announcement-demo"
EVENTS_KEY = "events.json"

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
        title = body.get('title')
        date = body.get('date')
        description = body.get('description')

        if not title or not date or not description:
            return {
                "statusCode": 400,
                "headers": headers,
                "body": json.dumps({"error": "Title, date and description are required"})
            }

        try:
            obj = s3_client.get_object(Bucket=BUCKET_NAME, Key=EVENTS_KEY)
            events = json.loads(obj['Body'].read().decode('utf-8'))
        except s3_client.exceptions.NoSuchKey:
            events = []

        events.append({"title": title, "date": date, "description": description})

        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=EVENTS_KEY,
            Body=json.dumps(events),
            ContentType='application/json'
        )

        message = f"New Event Added!\n\nTitle: {title}\nDate: {date}\nDescription: {description}"
        sns_client.publish(TopicArn=SNS_TOPIC_ARN, Message=message, Subject="New Event")

        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({"message": "Event created and notification sent!"})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"error": str(e)})
        }
