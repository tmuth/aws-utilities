# This script:
# - Gets the public IP and tag=name for each of your running instances
# - Adds to or updates /etc/hosts with those entries
# You'll want to setup boto3 credenitals to get it working: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html 

from python_hosts import Hosts, HostsEntry
from collections import defaultdict
import boto3

hosts = Hosts(path='/etc/hosts')

def writeEntry(name,ip):
    new_entry = HostsEntry(entry_type='ipv4', address=ip, names=[name])
    hosts.add([new_entry],force=True)
    hosts.write()

# Connect to EC2
ec2 = boto3.resource('ec2')

# Get information for all running instances
running_instances = ec2.instances.filter(Filters=[{
    'Name': 'instance-state-name',
    'Values': ['running']}])

ec2info = defaultdict()
for instance in running_instances:
    for tag in instance.tags:
        if 'Name'in tag['Key']:
            name = tag['Value']
    # Add instance info to a dictionary         
    ec2info[instance.id] = {
        'Name': name,
        'Type': instance.instance_type,
        'State': instance.state['Name'],
        'Private IP': instance.private_ip_address,
        'Public IP': instance.public_ip_address,
        'Launch Time': instance.launch_time
        }

attributes = ['Name', 'Type', 'State', 'Private IP', 'Public IP', 'Launch Time']
for instance_id, instance in ec2info.items():
    for key in attributes:
        print("{0}: {1}".format(key, instance[key]))
    print("------")

for instance_id, instance in ec2info.items():
    print(instance['Public IP']+'\t'+instance['Name'])
    writeEntry(instance['Name'],instance['Public IP'])
