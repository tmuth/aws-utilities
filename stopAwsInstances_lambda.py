import boto3
import json
# Enter the region your instances are in. Include only the region without specifying Availability Zone; e.g., 'us-east-1'
region = 'us-east-1'

def lambda_handler(event, context):
    
    ec2 = boto3.resource('ec2')
    filters = [
        {
        'Name': 'instance-state-name', 
        'Values': ['running']                 # pending | running | shutting-down | terminated | stopping | stopped
        }
    ]
    
    instances = ec2.instances.filter(Filters = filters)
    instanceJSON = []
    RunningInstances = []
    instanceList = []
    for instance in instances:
        instancename = ''
        try:
            for tags in instance.tags:
                if tags["Key"] == 'Name':
                    instancename = ', name:'+tags["Value"]
        except:
            pass
        
        RunningInstances.append('Stopping id: '+instance.id+instancename)
        instanceList.append(instance.id)
    
    print(instanceList)
    if len(instanceList):
        try:
            ec2 = boto3.client('ec2', region_name=region)
            ec2.stop_instances(InstanceIds=instanceList)
            RunningInstances.append('Stopped instances')
        except:
            RunningInstances.append('Error in stopping instances')
            pass
    else:
        # this is the case where there are no running instances
        RunningInstances.append('No running instances')
    
    instanceJSON = json.dumps(RunningInstances)
    print(instanceJSON)
    return {
        "statusCode": 200,
        "body": instanceJSON
    }