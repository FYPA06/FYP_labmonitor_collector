import boto3
import json
import os
import datetime
import  requests

print('Loading function')
# Get the service client
s3 = boto3.client('s3')
apigateway = boto3.client('apigateway')

def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def lambda_handler(event, context):
    apiKey = apigateway.get_api_key(apiKey=event["requestContext"]["identity"]["apiKeyId"],includeValue=True)

    now = datetime.datetime.now()
    partition = now.strftime("year=%Y/month=%m/day=%d/hour=%H")
    filename = now.strftime("Screenshot_%M_%S.jpg")
    
    Bucket= os.environ['StudentLabDataBucket']
    Key=f"screenshot_stream/{partition}/id={apiKey['name']}/{filename}"
    fields = {"acl": "public-read"}


    conditions = [
        {"acl": "public-read"}
        
        ]


    post = s3.generate_presigned_post(
        Bucket=Bucket,
        Key=Key,
        Fields=fields,
        Conditions=conditions
        )

    # Return the presigned URL
    return respond(None, post)
    