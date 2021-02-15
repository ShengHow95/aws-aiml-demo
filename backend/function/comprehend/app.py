import os
import json
import boto3

comprehendClient = boto3.client('comprehend')
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

        if requestBody['detection'] == 'Dominant Language Detection':
            response = comprehendClient.detect_dominant_language(
                Text = requestBody['text'],
            )
            result['Languages'] = response['Languages']
        elif requestBody['detection'] == 'Entities Detection':
            response = comprehendClient.detect_entities(
                Text = requestBody['text'],
                LanguageCode = requestBody['languageCode']
            )
            result['Entities'] = response['Entities']
        elif requestBody['detection'] == 'Key Phrases Detection':
            response = comprehendClient.detect_key_phrases(
                Text = requestBody['text'],
                LanguageCode = requestBody['languageCode']
            )
            result['KeyPhrases'] = response['KeyPhrases']
        elif requestBody['detection'] == 'PII Entities Detection':
            response = comprehendClient.detect_pii_entities(
                Text = requestBody['text'],
                LanguageCode = requestBody['languageCode']
            )
            result['Entities'] = response['Entities']
        elif requestBody['detection'] == 'Sentiment Detection':
            response = comprehendClient.detect_sentiment(
                Text = requestBody['text'],
                LanguageCode = requestBody['languageCode']
            )
            result['Sentiment'] = response['Sentiment']
            result['SentimentScore'] = response['SentimentScore']
        elif requestBody['detection'] == 'Syntax Detection':
            response = comprehendClient.detect_syntax(
                Text = requestBody['text'],
                LanguageCode = requestBody['languageCode']
            )
            result['SyntaxTokens'] = response['SyntaxTokens']
        
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
