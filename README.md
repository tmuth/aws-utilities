# aws-utilities
These utilities fall under two major categories:
- A lambda function (written in python) that runs in AWS on a nightly basis to shut down all running EC2 instances. This is to save on AWS costs from accidentally leaving an instance running.
- A python script that runs locally on a laptop to provide a suite of helper utilities to make working with AWS easier (at least for me) including:
    - View a list of your EC2 instances and their state (running, stopped, etc)
    - Stop or start any of your EC2 instances
    - Update your local `/etc/hosts` file with the name and public IP of any running EC2 instances
    - Update a named security group policy with your current public IP to allow access only your laptop

## Lambda function setup
- Follow [this guide](https://aws.amazon.com/premiumsupport/knowledge-center/start-stop-lambda-eventbridge/) from AWS to create an IAM Policy, lambda function, and EventBridge rule. 
- Replace the example python code for the lambda function with the code in [stopAwsInstances_lambda.py](stopAwsInstances_lambda.py)

## Local utility setup
### Pre-requirements
1. Install the AWS CLI either using [this guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) or via homebrew for Mac using `brew install awscli`
2. Follow the instructions in [this guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-prereqs.html) to configure AWS authentication.
3. Test configuration from a terminal with the following command to list your EC2 instances:
~~~
aws ec2 describe-instances --query 'Reservations[*].Instances[*].{ID:InstanceId,Name:Tags[?Key==`Name`]|[0].Value,State:State.Name}' --output text
~~~

### Local utility configuration
1. Install python3 packages via pip3:
`pip3 install python_hosts,boto3, simple_term_menu`
2. Download `aws-menu.py` and `update-hosts.py` into a scripts directory in your home directory. 
3. The "Update /etc/hosts" functionality uses sudo to run update-hosts.py. To enable this command without requiring a password each time, run the following from a terminal to create a new file called aws-menu in `/private/etc/sudoers.d` and add an entry to it to allow the script to run using sudo:
`sudo visudo /private/etc/sudoers.d/aws-menu`
and add the following line to that file (substitue your user and the path of the file):
`tmuth            ALL = (ALL) NOPASSWD: /usr/local/bin/python3 /Users/tmuth/scripts/update-hosts.py`
4. Save and exit visudo
5. Run it via `python3 aws-menu.py`
6. Optionally add a bash alias to make it easier to run:
`alias aws-menu='python3 ~/scripts/aws-menu.py'`
