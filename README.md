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

### Setup Integration with API Gateway
TODO

### Test Integration
TODO

### Edit Lambda Handler
TODO

### Log Flask Output
TODO

