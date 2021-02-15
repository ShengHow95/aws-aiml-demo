import os
import json
import boto3

ddbTableClient = boto3.resource('dynamodb').Table(os.getenv('DDBTable'))
pkey = ddbTableClient.key_schema[0]['AttributeName']

def lambda_handler(event, context):
    
    print(event)
    
    requestParameters = event['queryStringParameters']
    result = dict()
    
    try:
        
        apiCount = ddbTableClient.get_item(Key = { pkey: 'username#'+requestParameters['username']})['Item']['apiCount']
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
            'body': json.dumps({"message": str(e)})
        }
