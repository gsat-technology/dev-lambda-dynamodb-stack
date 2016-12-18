import logging
import json
  
import boto3
import botocore
from flask import Flask
from flask import request

from nocache import nocache
from printer import printer
from dynamodb.actions import create_table, put_item, get_item, delete_table
from lambda_handler.lambda_handler import lambda_handler as lam

app = Flask(__name__)

@app.route("/lambda", methods=['POST'])
@nocache
def lambda_handler():
    printer('serving request to /lambda')

    #convert body data (our event) to python object
    try:
        event = json.loads(request.data)
    except ValueError as e:
        #couldn't convert
        printer(e)
        return "error. check docker logs"

    #hand off to the lambda stand-in
    response = lam(event, None)    

    return json.dumps(response)

    
@app.route("/testdynamodb")
@nocache
def testdynamodb():
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
