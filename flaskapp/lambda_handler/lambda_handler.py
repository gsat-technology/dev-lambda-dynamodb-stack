
#Note: print debug statements to stderr using:
#print >> sys.stderr, 'my log statement'
#run docker logs -f <container id> to watch live log stream


import json
import sys

#below is a function to neaten things up
def printer(msg):
    print >> sys.stderr, msg
    
#this function is intended to simulate what would be run in Lambda
#note that there is no 'context'
def lambda_handler(event, context):

    printer('lambda_handler recieved event: {}'.format(json.dumps(event)))

    return event
