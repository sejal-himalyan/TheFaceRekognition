# TheFaceRekognition

I built a simple Face Detection System using AWS services! This project automatically detects faces in images and sends a notification when a face is found. No servers needed—just serverless computing!

How It Works?
 Upload an Image → Stored in Amazon S3
 AWS Lambda gets triggered → Sends the image to Amazon Rekognition
 Rekognition analyzes the image → Detects faces, emotions & features
 AWS SNS sends a notification if a face is detected
