#!/bin/env python

import boto3
dynamodb_endpoint='http://localhost:8000'

ddb_client = boto3.client('dynamodb',
                          aws_access_key_id="anything",
                          aws_secret_access_key="anything",
                          endpoint_url=dynamodb_endpoint,
                          region_name='ap-southeast-2')

table = ddb_client.create_table(
    TableName='user',
    KeySchema=[
        {
            'AttributeName': 'id',
            'KeyType': 'HASH'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'id',
            'AttributeType': 'S'
        },
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
)

if table['TableDescription']['TableStatus'] == 'ACTIVE':
    print 'okay'
else:
    print 'error creating dyanamo_db table'

