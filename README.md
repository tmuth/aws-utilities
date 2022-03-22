# aws-utilities


## Lambda function setup
(needs better documentation)
- Create a new AWS lambda function with the file stopAwsInstances_lambda.py via the AWS console 
- Use the file lambda_permissions_policy.json to define the permissions

## Local utility setup
- Setup the AWS CLI either using [this guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) or via homebrew for Mac using `brew install awscli`
1. Follow the instructions in [this guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-prereqs.html) to setup AWS authentication 
2. Install python3 packages via pip3 (will update with list)
3. The "Update /etc/hosts" functionality uses sudo to run update-hosts.py. To enable this command without requiring a password each time, run the following... (visudo, etc, etc)
4. Run it via `python3 aws-menu.py`, which also calls update-hosts.py via sudo 
