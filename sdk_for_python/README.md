# AWS **SDK** for **Python**

## Objective

1. Create a VPC with two subnets, one public and one private, with AWS SDK for python

2. Launch an EC2 instance with AWS SDK for python

## Prerequisite

1. Install python packages `boto3` and `awscli` on local machine

2. Configure AWS credentials locally, running `aws configure` from a terminal.
This will create

    - a file `~/.aws/credentials` with the Access Key ID and the Secret Access Key
    - a file `~/.aws/config` with the default region

    We can test that everything works fine by typing in the console `aws ec2 describe-instances`

## Setting up the network architecture

### Creating a VPC

1. We first import the `boto3` library in Python  and create an `ec2` resource object
using the method `resource()`

2. Then we create a VPC using the `create_vpc()` method

3. To add tags to the VPC, we use the method `create_tags()`

```python
import boto3

cidr_vpc = '10.0.0.0/16'

# create an ec2 ressource object
ec2 = boto3.resource('ec2')

# create a VPC
vpc = ec2.create_vpc(CidrBlock=cidr_vpc)

# assign a name to the VPC
vpc.create_tags(Tags=[{"Key": "Name", "Value": "my_vpc"}])

vpc.wait_until_available()
```

### Creating an Internet Gateway

```python
# create an IGW and attach it to the VPC
igw = ec2.create_internet_gateway()
igw.create_tags(Tags=[{"Key": "Name", "Value": "my_igw"}])
vpc.attach_internet_gateway(InternetGatewayId=igw.id)
```

### Creating the subnets 

1. We identify the main route table of the VPC for the private subnet.
We also create, with `create_route_table()`, a route table for the public subnet
and establish a public route

```python
# identify main route table
main_vpc_rt = []
for route_table in vpc.route_tables.all():
    for association in route_table.associations:
        if association.main:
            main_vpc_rt.append(route_table)
rt_main = main_vpc_rt[0]
rt_main.create_tags(Tags=[{"Key": "Name", "Value": "my_rt_private"}])

# create a route table for public subnet 
rt_public = vpc.create_route_table()
rt_public.create_tags(Tags=[{"Key": "Name", "Value": "my_rt_public"}])

# add a public route to the public route table
route_public = rt_public.create_route(DestinationCidrBlock='0.0.0.0/0', GatewayId=igw.id)
```

2. We create the two subnets with the method `create_subnet()`

```python
cidr_sn_public = '10.0.1.0/24'
cidr_sn_private = '10.0.2.0/24'

# public subnet
sn_public = ec2.create_subnet(CidrBlock=cidr_sn_public, VpcId=vpc.id)
sn_public.create_tags(Tags=[{"Key": "Name", "Value": "my_sn_public"}])

# private subnet
sn_private = ec2.create_subnet(CidrBlock=cidr_sn_private, VpcId=vpc.id)
sn_private.create_tags(Tags=[{"Key": "Name", "Value": "my_sn_private"}])
```

3. It remains to attach the route tables to the subnets

```python
rt_main.associate_with_subnet(SubnetId=sn_private.id)
rt_public.associate_with_subnet(SubnetId=sn_public.id)
```

## Launch an EC2 instance

### Creating a security group for SSH only

```python
# create a security group and allow SSH inbound rule through the VPC
sg = ec2.create_security_group(GroupName='SSH-ONLY', Description='only allow SSH traffic', VpcId=vpc.id)
sg.authorize_ingress(CidrIp='0.0.0.0/0', IpProtocol='tcp', FromPort=22, ToPort=22)
sg.create_tags(Tags=[{"Key": "Name", "Value": "my_sg"}])
```

### Creating the EC2 instance

We create an EC2 `t2.micro` instance in the public subnet.
**Do not forget** to put a valid key-pair file `ec2-keypair.pem` in the current working directory
of the local machine

```python
instance = ec2.create_instances(
    ImageId='ami-00068cd7555f543d5',
    InstanceType='t2.micro',
    MaxCount=1,
    MinCount=1,
    NetworkInterfaces=[{
        'SubnetId': sn_public.id,
        'DeviceIndex': 0,
        'AssociatePublicIpAddress': True,
        'Groups': [sg.group_id]
    }],
    KeyName='ec2-keypair'
)

# ec2.create_instance() returns a list of instances
instance[0].create_tags(Tags=[{"Key": "Name", "Value": "my_ec2"}])
```
