# pip3 install python_hosts,boto3
from python_hosts import Hosts, HostsEntry
from collections import defaultdict
import boto3
import pprint
import time
import os

# User set variables
region='us-east-1'


# Global variables
selectedInstanceID=''
selectedInstanceMenuNum=-1
selectedAction=''
instanceList=[]
ec2info = defaultdict()



def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def listInstances():
    ec2 = boto3.resource('ec2')
    # Get information for all running instances
    running_instances = ec2.instances.filter()
    global ec2info
    i=0
    for instance in running_instances:
        for tag in instance.tags:
            if 'Name'in tag['Key']:
                name = tag['Value']
        # Add instance info to a dictionary   
        i = i + 1      
        ec2info[i] = {
            'ID': instance.id,
            'Name': name,
            'Type': instance.instance_type,
            'State': instance.state['Name'],
            'PublicIP': str(instance.public_ip_address),
            'LaunchTime': instance.launch_time
            }

    
    attributes = ['#','ID','Name', 'Type', 'State', 'PublicIP', 'LaunchTime']
    print ("\n{:<3} {:<20} {:<20} {:<15} {:<10} {:<20} {:<30}".format(*attributes))
    for key in ec2info:
        item = ec2info[key]
        lineFormatted="{:<3} {:<20} {:<20} {:<15} {:<10} {:<20} {}".format(key,item['ID'] ,item['Name'],item['Type'],item['State'],item['PublicIP'],item['LaunchTime'])

        instanceList.append(lineFormatted)
        print(lineFormatted)

    print("\n\n")



def loopInstances(loops,sleepSec):
    i = 1
    while i <= loops:
        cls()
        print("Loop "+str(i))
        listInstances()
        time.sleep(sleepSec)
        i += 1
        
        



def controlInstance():
    print("Instance ID: "+selectedInstanceID)
    
    ec2Client = boto3.client('ec2', region_name=region)
    resp = ec2Client.describe_instance_status(
            InstanceIds=[str(selectedInstanceID)],
            IncludeAllInstances=True)

    print("Response = ",resp)

    instance_status = resp['InstanceStatuses'][0]['InstanceState']['Code']

    #print("Instance status =", instance_status)

    if instance_status == 80:
        ec2Client.start_instances(InstanceIds=[selectedInstanceID])
        print("Started instance with Instance_id",selectedInstanceID)

    elif instance_status == 16:
         ec2Client.stop_instances(InstanceIds=[selectedInstanceID])
         print("Stopped EC2 with Instance-ID",selectedInstanceID)
    else:
         print("No desired state found")
    #print("Response = ",resp)
    loopInstances(20,2)



from simple_term_menu import TerminalMenu

def actionMenu():
    print(selectedInstanceID)
    options = ["start", "stop"]
    terminal_menu = TerminalMenu(options)
    #terminal_menu = TerminalMenu(instanceList)
    menu_entry_index = terminal_menu.show()
    selectedAction=options[menu_entry_index]
    print(selectedAction)
    controlInstance(selectedAction)

def mainMenu():
    options = ["view", "toggle"]
    terminal_menu = TerminalMenu(options)
    #terminal_menu = TerminalMenu(instanceList)
    menu_entry_index = terminal_menu.show() 

    if options[menu_entry_index] == "view":
        loopInstances(20,2)
    else:
        instanceMenu()


def instanceMenu():
    #options = ["entry 1", "entry 2", "entry 3"]
    #terminal_menu = TerminalMenu(options)
    terminal_menu = TerminalMenu(instanceList)
    menu_entry_index = terminal_menu.show()
    print(f"You have selected\n {instanceList[menu_entry_index]}!")
    selectedItem = instanceList[menu_entry_index]
    selectedInstanceMenuNum=int(selectedItem[0:1])
    global selectedInstanceID
    selectedInstanceID=ec2info[selectedInstanceMenuNum]['ID']
    #print(selectedInstanceID)
    #print("ID: "+ec2info[selectedInstanceMenuNum]['ID'])
    controlInstance()

if __name__ == "__main__":
    listInstances()
    mainMenu()
