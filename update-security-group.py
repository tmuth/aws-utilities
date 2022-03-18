from python_hosts import Hosts, HostsEntry
from collections import defaultdict
import boto3
import urllib.request
import pprint
import json

# Either create a security group with this name or change it to the name of your security group
sgName = ['laptop-aws']

external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
print(external_ip)

from botocore.exceptions import ClientError

ec2 = boto3.client('ec2')

try:
    response = ec2.describe_security_groups(GroupNames=sgName)
   # print(response)
    group_id = response['SecurityGroups'][0]['GroupId']

    ec2Resource = boto3.resource('ec2')
    sg = ec2Resource.SecurityGroup(group_id)
    if sg.ip_permissions:
        sg.revoke_ingress(IpPermissions=sg.ip_permissions)

except ClientError as e:
    print(e)

try:
    #ec2 = boto3.client('ec2')
    response = ec2.describe_security_groups(GroupNames=sgName)
    #print(response)
    group_id = response['SecurityGroups'][0]['GroupId']

    data = ec2.authorize_security_group_ingress(
        GroupId=group_id,
        IpPermissions=[
            {'IpProtocol': 'tcp',
             'FromPort': 8000,
             'ToPort': 9000,
             'IpRanges': [{'CidrIp': external_ip+'/32'}]},
            {'IpProtocol': 'tcp',
             'FromPort': 22,
             'ToPort': 22,
             'IpRanges': [{'CidrIp': external_ip+'/32'}]}
        ])
    print()
    print(f'Successfully updated rules for {sgName[0]} security group')
    #pprint.pprint(data['SecurityGroupRules'])

    ruleInfo = defaultdict()
    for sgRule in data['SecurityGroupRules']:


        attributes = ['CidrIpv4', 'FromPort','ToPort']
        for key in attributes:
            print("{0}: {1}".format(key, sgRule[key]))
        print("---------------------------")
      


except ClientError as e:
    print(e)