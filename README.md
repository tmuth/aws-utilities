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
- Replace the example python code for the lambda function with the code in `stopAwsInstances_lambda.py`

## Local utility setup
- Setup the AWS CLI either using [this guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) or via homebrew for Mac using `brew install awscli`
1. Follow the instructions in [this guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-prereqs.html) to setup AWS authentication 
2. Install python3 packages via pip3 (will update with list)
3. The "Update /etc/hosts" functionality uses sudo to run update-hosts.py. To enable this command without requiring a password each time, run the following... (visudo, etc, etc)
4. Run it via `python3 aws-menu.py`, which also calls update-hosts.py via sudo 
