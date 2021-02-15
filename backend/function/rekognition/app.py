import os
import json
import boto3

S3BUCKET = os.getenv('S3Bucket')
rekognitionClient = boto3.client('rekognition')
ddbTableClient = boto3.resource('dynamodb').Table(os.getenv('DDBTable'))
pkey = ddbTableClient.key_schema[0]['AttributeName']


def lambda_handler(event, context):
    
    requestBody = json.loads(event['body'])
    result = dict()
    
    try:
        apiCount = ddbTableClient.get_item(Key = { pkey: 'username#'+requestBody['username']})['Item']['apiCount']
        
        if int(apiCount) == 0:
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({ 'errorMessage': 'You have reached your maximum number of API Calls. Please contact administrator if you require more API Calls.' })
            }
        else:
            apiCount = ddbTableClient.update_item(
                Key = { pkey: 'username#'+requestBody['username']},
                UpdateExpression = 'set apiCount=:a',
                ExpressionAttributeValues={ ':a': int(apiCount)-1 },
                ReturnValues="UPDATED_NEW"
            )['Attributes']['apiCount']

        if requestBody['detection'] == 'Object Detection':
            response = rekognitionClient.detect_labels(
                Image = {
                    'S3Object': {
                        'Bucket': S3BUCKET,
                        'Name': 'picture/' + requestBody['image']
                    }
                }
            )
            result['Labels'] = response['Labels']
        elif requestBody['detection'] == 'Text Recognition':
            response = rekognitionClient.detect_text(
                Image = {
                    'S3Object': {
                        'Bucket': S3BUCKET,
                        'Name': 'picture/' + requestBody['image']
                    }
                }
            )
            result['TextDetections'] = response['TextDetections']
        
        result['apiCount'] = int(apiCount)
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps(result)
        }

    except Exception as e:
        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({"Message": str(e)})
        }
