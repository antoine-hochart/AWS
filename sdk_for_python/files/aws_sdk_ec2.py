import boto3

# create an ec2 ressource object
ec2 = boto3.resource('ec2')

vpc_name = 'my_vpc'
sn_name = 'my_sn_public'

# retrieve VPC based on name tag
filters = [{'Name': 'tag:Name', 'Values': [vpc_name]}]
vpcs = list(ec2.vpcs.filter(Filters=filters))
myvpc = vpcs[0]

# retrieve subnet based on name tag
filters = [{'Name': 'tag:Name', 'Values': [sn_name]}]
subs = list(myvpc.subnets.filter(Filters=filters))
mysub = subs[0]

# create a security group for SSH only
sg = ec2.create_security_group(GroupName='SSH-ONLY', Description='only allow SSH traffic', VpcId=myvpc.id)
sg.authorize_ingress(CidrIp='0.0.0.0/0', IpProtocol='tcp', FromPort=22, ToPort=22)
sg.create_tags(Tags=[{"Key": "Name", "Value": "my_sg"}])

# launch an ec2 instance
# CHANGE ec2-keypair IF NECESSARY
instance = ec2.create_instances(
    ImageId='ami-00068cd7555f543d5',
    InstanceType='t2.micro',
    MaxCount=1,
    MinCount=1,
    NetworkInterfaces=[{
        'SubnetId': mysub.id,
        'DeviceIndex': 0,
        'AssociatePublicIpAddress': True,
        'Groups': [sg.id]
    }],
    KeyName='ec2-keypair'
)

# ec2.create_instance() returns a list of instances
instance[0].create_tags(Tags=[{"Key": "Name", "Value": "my_ec2"}])

instance[0].wait_until_running()
