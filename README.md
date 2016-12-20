## dev-lambda-dynamodb-stack

For lambda _python_ development purposes (esp. when working with API Gateway) replace Lambda integration with EC2 instance running Flask. The goal of this is to be able to test and iterate code faster without the need to wait for CloudWatch Logs to refresh.

Also includes a dockerised DynamoDB container (you don't _have_ to use this though - it's just there if you need it)

CloudFormation template deploys an EC2 instance with:

- Flask docker container
- Local Dynamodb docker container

![alt tag](https://raw.githubusercontent.com/gsat-technology/dev-lambda-dynamodb-stack/master/resources/high-level-architecture-diagram.png)

![alt tag](https://raw.githubusercontent.com/gsat-technology/dev-lambda-dynamodb-stack/master/resources/ec2-detail-diagram.png)

### Launch CloudFormation Stack

Using the AWS CloudFormation console, upload `cloudformation/cf.yml` and choose parameter values as required

Or, using the CLI

```
git clone https://github.com/gsat-technology/dev-lambda-dynamodb-stack.git
cd dev-lambda-dynamodb-stack/cloudformation

EC2_TYPE=t2.nano
AMI="" #add ubuntu 16.04 ubuntu image (appropriate ami for target region)
VPC="" #your VPC id
SSH_CIDR="0.0.0.0/0" # replace as needed
KEY_PAIR="" #your existing keypair

aws cloudformation create-stack \
    --stack-name devlambda2 \
    --template-body file://cf.yml \
    --parameters ParameterKey=InstanceTypeParameter,ParameterValue=$EC2_TYPE \
                 ParameterKey=UbuntuAMIParameter,ParameterValue=$AMI \
                 ParameterKey=VPCParameter,ParameterValue=$VPC \
                 ParameterKey=SSHCIDRParamter,ParameterValue=$SSH_CIDR \
                 ParameterKey=KeyPairParameter,ParameterValue=$KEY_PAIR
```

On launch, EC2 instance will automatically install, configure and start the containers. 

Note that installation of docker and building of containers may take a little while. You can tail the cloud-init-output.log file to check on the progress:

```
tail -f /var/log/cloud-init-output.log
```

The docker containers starting up is the final action.

####Simple Test

Get the public IP address of your EC2 instance and try sending a POST request to /lambda on port 5000 i.e.

```
curl -H "Content-Type: application/json" -X POST -d '{"message":"it works!"}' http://<ec2_ip_address>:5000/lambda
```

The response you should receive is the same JSON you passed in the POST body i.e. `{"message":"it works!"}`

####Test DynamoDB

Try the test endpoint to ensure that the DynamoDB container is reachable. The test endpoint simply creates a new table, adds an item, gets the item, then deletes the table.

```
curl -v 'http://<ec2_ip_address>:5000/testdynamodb?tablename=xyz&id=999&somestring=heya'
```

The above should produce this response

```json
{
  "put_item": "OK",
  "delete_table": "OK",
  "create_table": "OK",
  "get_item": {
    "somestring": "heya",
    "id": "999"
  }
}
```

### Setup Integration with API Gateway
TODO

### Test Integration
TODO

### Edit Lambda Handler
TODO

### Log Flask Output

Logging from Flask (and the mock lambda_handler.py function) can be tailed from the flask docker container e.g.

1. Get the id of the flask container by
running `docker ps` and note the id of the `devlambdadynamodbstack_flask ` container

2. Tail the log of the flask container

```
docker logs -f <container id>
```

Or the above in a one-liner:

```
docker logs -f $(docker ps -aqf "name=devlambdadynamodbstack_flask")
```


 

