# aws-utilities

## Lambda function setup
(needs better documentation)
- Create a new AWS lambda function with the file stopAwsInstances_lambda.py via the AWS console 
- Use the file lambda_permissions_policy.json to define the permissions

## Local utility setup
- Setup the AWS CLI either using [this guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) or via homebrew for Mac using brew install awscli
- Follow the instructions in [this guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-prereqs.html) to setup AWS authentication 
- Install python3 packages via pip3 (will update with list)
- Run it via `python3 aws-menu.py`, which also calls update-hosts.py via sudo 
