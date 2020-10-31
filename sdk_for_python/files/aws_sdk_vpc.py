import boto3

# CIDR for VPC and Subnets
cidr_vpc = '10.0.0.0/16'
cidr_sn_public = '10.0.1.0/24'
cidr_sn_private = '10.0.2.0/24'

# crete an ec2 ressource object
ec2 = boto3.resource('ec2')

# create a VPC
vpc = ec2.create_vpc(CidrBlock=cidr_vpc)

# assign a name to the VPC
vpc.create_tags(Tags=[{"Key": "Name", "Value": "my_vpc"}])

vpc.wait_until_available()

# create an IGW and attach it to the VPC
igw = ec2.create_internet_gateway()
igw.create_tags(Tags=[{"Key": "Name", "Value": "my_igw"}])
vpc.attach_internet_gateway(InternetGatewayId=igw.id)

# identify the main route table
main_vpc_rt = []
for route_table in vpc.route_tables.all():
    for association in route_table.associations:
        if association.main:
            main_vpc_rt.append(route_table)
# main_vpc_rt = vpc.route_tables.filter(Filters=[{'Name': 'association.main', 'Values': ["true"]}])
rt_main = main_vpc_rt[0]
rt_main.create_tags(Tags=[{"Key": "Name", "Value": "my_rt_private"}])

# create a route table for the public subnet 
rt_public = vpc.create_route_table()
rt_public.create_tags(Tags=[{"Key": "Name", "Value": "my_rt_public"}])

# add a public route to the public route table
route_public = rt_public.create_route(DestinationCidrBlock='0.0.0.0/0', GatewayId=igw.id)

# create a public subnet
sn_public = ec2.create_subnet(CidrBlock=cidr_sn_public, VpcId=vpc.id)
sn_public.create_tags(Tags=[{"Key": "Name", "Value": "my_sn_public"}])

# create a private subnet
sn_private = ec2.create_subnet(CidrBlock=cidr_sn_private, VpcId=vpc.id)
sn_private.create_tags(Tags=[{"Key": "Name", "Value": "my_sn_private"}])

# attach the route tables to the subnets
rt_main.associate_with_subnet(SubnetId=sn_private.id)
rt_public.associate_with_subnet(SubnetId=sn_public.id)
