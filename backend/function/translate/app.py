import os
import json
import boto3

translateClient = boto3.client('translate')
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
        
        response = translateClient.translate_text(
            Text=requestBody['text'],
            SourceLanguageCode=requestBody['sourceLanguageCode'],
            TargetLanguageCode=requestBody['targetLanguageCode']
        )
        
        result['TranslatedText'] = response['TranslatedText']
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
