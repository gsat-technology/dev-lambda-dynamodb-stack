import logging
import json
 

import boto3
import botocore
from flask import Flask
from flask import request

from nocache import nocache
from printer import printer

app = Flask(__name__)

dynamodb_endpoint='http://dynamodb:8000'

ddb_client = boto3.client('dynamodb',
                          aws_access_key_id="anything",
                          aws_secret_access_key="anything",
                          endpoint_url=dynamodb_endpoint,
                          region_name='ap-southeast-2')

ddb_resource = boto3.resource('dynamodb',
                              aws_access_key_id="anything",
                              aws_secret_access_key="anything",
                              endpoint_url=dynamodb_endpoint,
                              region_name='ap-southeast-2')

def create_table(table_name):

    try:
        table = ddb_client.create_table(
            TableName=table_name,
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
            return "OK"
        else:
            printer('table not created')
            return "FAIL"
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            printer('table already exists')

        return "FAIL"


def put_item(table, item):
    user_table = ddb_resource.Table(table)
    response = user_table.put_item(Item=item)

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return "OK"
    else:
        printer(response)
        return "FAIL"
    

def get_item(table_name, _id):
    table = ddb_resource.Table(table_name)
    response = table.get_item(Key={'id': _id})

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return response['Item']
    else:
        return "FAIL"


def delete_table(table):
    
    try:
        response = ddb_client.delete_table(TableName=table)
        
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return "OK"
        else:
            printer(response)
            return "FAIL"
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print('cannot delete table (does not exist)')

    return "FAIL"

    
@app.route("/testdynamodb")
@nocache
def test():
    printer('serving request to /testdynamodb')
    #retrieve GET params from request
    table = request.args.get('tablename')
    _id = request.args.get('id')
    somestring = request.args.get('somestring')

    if not table or not _id or not somestring:
        print('incorrect params supplied')
        return json.dumps({"error": "'tablename',  'id', 'somestring' must be supplied as GET params"})

    printer('table: %s' % table)
    printer('id: %s' % _id)
    printer('somestring: %s' % somestring)
    
    item = {
        'id': _id,
        'somestring': somestring
    }
    
    r = {
        'create_table': create_table(table),
        'put_item': put_item(table, item),
        'get_item': get_item(table, _id),
        'delete_table': delete_table(table)
    }

    return json.dumps(r)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
