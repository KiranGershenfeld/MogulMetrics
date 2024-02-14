import json
import requests
def lambda_handler(event, context):
    res = requests.get("http://ec2-18-117-130-175.us-east-2.compute.amazonaws.com:5000/refresh_subscriptions")
    return {
        'statusCode': 200,
        'body': "Hit refresh subscription endpoint"
    }
