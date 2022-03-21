# pip3 install python_hosts,boto3, simple_term_menu
from python_hosts import Hosts, HostsEntry
from collections import defaultdict
from simple_term_menu import TerminalMenu
import boto3
import pprint
import time
import os
import signal
import sys
import urllib.request
from botocore.exceptions import ClientError



# User set variables
region='us-east-1'
securityGroupName = ['laptop-aws']


# Global variables
selectedInstanceID=''
selectedInstanceMenuNum=-1
selectedAction=''
instanceList=[]
ec2info = defaultdict()


def signal_handler(signum, frame):
    signal.signal(signum, signal.SIG_IGN) # ignore additional signals
    #cleanup() # give your process a chance to clean up
    sys.exit(0)

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

cls() 

def listInstances(instance_id=None):
    ec2 = boto3.resource('ec2')
    # Get information for all running instances
    if instance_id is not None:
        #filterId=list(instance_id)
        filterId=list(instance_id.split(" "))
        #print(filterId)
        #time.sleep(3)
        running_instances = ec2.instances.filter(InstanceIds=filterId)
    else:
        running_instances = ec2.instances.filter()
    global ec2info
    global instanceList
    instanceList = []
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

def loopInstanceUntilState(instance_id_filter,state):
    i = 1
    sleepSec=2
    while True:
        global ec2info
        ec2info.clear()
        cls()
        #print("Loop "+str(i))
        #print(instance_id_filter)
        #time.sleep(3)
        listInstances(instance_id=instance_id_filter)
        if ec2info[1]['State'] == state:
            break
        time.sleep(sleepSec)
        i += 1


def controlInstance():
    #print("Instance ID: "+selectedInstanceID)
    #time.sleep(5)
    
    ec2Client = boto3.client('ec2', region_name=region)
    resp = ec2Client.describe_instance_status(
            InstanceIds=[str(selectedInstanceID)],
            IncludeAllInstances=True)
    #print("Response = ",resp)

    instance_status = resp['InstanceStatuses'][0]['InstanceState']['Code']

    if instance_status == 80:
        ec2Client.start_instances(InstanceIds=[selectedInstanceID])
        print("Started instance with Instance_id",selectedInstanceID)
        loopInstanceUntilState(instance_id_filter=selectedInstanceID,state="running")

    elif instance_status == 16:
         ec2Client.stop_instances(InstanceIds=[selectedInstanceID])
         print("Stopped EC2 with Instance-ID",selectedInstanceID)
         loopInstanceUntilState(instance_id_filter=selectedInstanceID,state="stopped")
    else:
         print("No desired state found")
    #print("Response = ",resp)
    #loopInstances(20,2)


def updateSecurityGroup(sgName):
    
    external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
    print("Your public IP address: "+external_ip)

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

def instanceMenu():
    #options = ["entry 1", "entry 2", "entry 3"]
    #terminal_menu = TerminalMenu(options)
    listInstances()
    terminal_menu = TerminalMenu(instanceList)
    menu_entry_index = terminal_menu.show()
    #print(f"You have selected\n {instanceList[menu_entry_index]}!")
    selectedItem = instanceList[menu_entry_index]
    selectedInstanceMenuNum=int(selectedItem[0:1])
    global selectedInstanceID
    selectedInstanceID=ec2info[selectedInstanceMenuNum]['ID']
    #print(selectedInstanceID)
    #print("ID: "+ec2info[selectedInstanceMenuNum]['ID'])
    controlInstance()


def mainMenu():
    menu_options = ["[v] view EC2 instances", "[s] start / stop EC2 instances",
                    "[u] update security group with my IP",
                    "[h] update /etc/hosts with AWS public IPs of running instances (sudo)",
                    "[t] test instance", "[x] exit"]
    main_menu_title = "  AWS Main Menu\n"
    main_menu_exit = False

    main_menu = TerminalMenu(
        menu_entries=menu_options,
        title=main_menu_title,
        #menu_cursor=main_menu_cursor,
        #menu_cursor_style=main_menu_cursor_style,
        #menu_highlight_style=main_menu_style,
        #cycle_cursor=True,
        shortcut_key_highlight_style=("fg_red", "bold"),
        clear_screen=False,
    )


    while not main_menu_exit:
        main_sel = main_menu.show()
        #print(main_sel)
        if menu_options[main_sel] == "[v] view EC2 instances":
            #loopInstances(1,2)
            listInstances()
        elif menu_options[main_sel] == "[s] start / stop EC2 instances":
            instanceMenu()
        elif menu_options[main_sel] == "[u] update security group with my IP":
            updateSecurityGroup(sgName=securityGroupName)
        elif menu_options[main_sel] == "[h] update /etc/hosts with AWS public IPs of running instances (sudo)":
            pathname = os.path.dirname(sys.argv[0]) 
            os.system('sudo python3 '+pathname+'/update-hosts.py')
        elif menu_options[main_sel] == "test instance":
            #listInstances(instance_id="i-0816b3092db695b9f")
            loopInstanceUntilState(instance_id="i-0816b3092db695b9f",state="running")
        elif menu_options[main_sel] == "[x] exit":
            main_menu_exit = True
            print("Exit Selected")
            quit()

if __name__ == "__main__":
    #listInstances()
    signal.signal(signal.SIGINT, signal_handler) # register the signal with the signal handler first
    mainMenu()