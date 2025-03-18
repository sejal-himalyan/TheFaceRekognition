import boto3
from decimal import Decimal
import json
import urllib.parse

print('Loading function')

rekognition = boto3.client('rekognition')
sns = boto3.client('sns')

SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:123456789012:FaceDetectionTopic"  # Replace with your SNS topic ARN

# --------------- Helper Functions ------------------

def detect_faces(bucket, key):
    response = rekognition.detect_faces(
        Image={"S3Object": {"Bucket": bucket, "Name": key}},
        Attributes=["ALL"]  # To get more detailed facial attributes
    )
    return response


def send_sns_notification(bucket, key, face_count):
    message = f"Face detection completed for image: {key} in bucket: {bucket}.\nTotal faces detected: {face_count}."
    
    response = sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Message=message,
        Subject="Face Detection Alert"
    )
    print(f"SNS Notification sent: {response}")


# --------------- Main Lambda Handler ------------------

def lambda_handler(event, context):
    '''Triggered when an image is uploaded to an S3 bucket.
       Calls Rekognition APIs and sends an SNS notification if faces are detected.
    '''
    print("Received event: " + json.dumps(event, indent=2))

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])

    try:
        response = detect_faces(bucket, key)
        face_count = len(response.get('FaceDetails', []))

        print(f"Faces detected: {face_count}")

        if face_count > 0:
            send_sns_notification(bucket, key, face_count)

        return {"status": "Success", "face_count": face_count}
    
    except Exception as e:
        print(f"Error processing {key} from bucket {bucket}: {str(e)}")
        raise e
