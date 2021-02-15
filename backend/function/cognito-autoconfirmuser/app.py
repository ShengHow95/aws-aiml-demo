import os
import boto3

ddbTableClient = boto3.resource('dynamodb').Table(os.getenv('DDBTable'))
pkey = ddbTableClient.key_schema[0]['AttributeName']

def lambda_handler(event, context):

    # Create user in DDB for API Usage Tracking
    item = {
        pkey: 'username#' + event['userName'],
        'apiCount': 30
    }
    ddbTableClient.put_item(Item=item)

    # Confirm the user
    event['response']['autoConfirmUser'] = True

    # Return to Amazon Cognito
    return event