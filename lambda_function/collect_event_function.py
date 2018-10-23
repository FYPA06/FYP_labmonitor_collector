import boto3
import json
import os
import datetime


print('Loading function')
s3 = boto3.client('s3')
apigateway = boto3.client('apigateway')
kinesis = boto3.client('kinesis')


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
    
    s3.put_object(Bucket=os.environ['StudentLabDataBucket'], Key="event_by_id/"+ apiKey["name"] + '/eventstream.json',
              Body=event["body"],
              Metadata={"ip":event["requestContext"]["identity"]["sourceIp"], },
              ContentType="application/json"
          )
    
    now = datetime.datetime.now()
    partition = now.strftime("year=%Y/month=%m/day=%d/hour=%H")
    filename = now.strftime("events_%M_%S.json")
    
    events = json.loads(event["body"])
    body = []
    Keyboad=[]
    Mouse=[]
    count=0
    for student_event in events:
        student_event["ip"] = event["requestContext"]["identity"]["sourceIp"]
        student_event["student"] = apiKey["description"]
        body.append(json.dumps(student_event) )
        del(student_event['time'],student_event['ip'],student_event['student'])
        if ((student_event["name"] == "KeyPressEvent") or (student_event["name"] == "KeyReleaseEvent")):
            Keyboad.append(student_event)
            count+=1

        else:
            Mouse.append(student_event)
            count+=1
        if count==500:
            putdatatokinesis(Mouse,"MouseEventStream",apiKey['name'])
            putdatatokinesis(Keyboad,"KeybroadEventStream",apiKey['name'])
          
            Mouse=[]
            keyboad=[]
            count=0
            

            
       
        
    s3.put_object(Bucket=os.environ['StudentLabDataBucket'], 
            Key = f"event_stream/{partition}/id={apiKey['name']}/{filename}",
            Body = '\n'.join(body).encode('utf8'),
            ContentType = "application/json"
          )
   
    return respond(None, apiKey["name"] + f" saved {len(events)} events.")
def putdatatokinesis(RecordKinesis,StreamNames,key):
        Record=[
        {
            'Data': b'RecordKinesis',
            'PartitionKey': key
        },
        ]
        
        response = kinesis.put_records(Records=Record, StreamName=StreamNames)
        return response    
