Mock Deployments
----------------
Mock deployments allow us to quickly create stacks with pre-configured parameters to test various stages of the integration of the resources involved. Note that deployment configs should not be commited to github for security reasons.

## Requirements
- Python 2.7+
- [AWS CLI](https://github.com/aws/aws-cli) - `pip install awscli` followed by `aws configure` to enter your default region (usually `us-east-1`) and your AWS access key
- [AWS CloudFormation CLI](https://github.com/Kotaimen/awscfncli) - `pip install awscfncli`

## Usage
1. Customize the example deployment config with values to fit the needs of your testing.
2. Deploy using `cfn stack deploy <path to deployment config>`, the stack will be created and stack events will be printed out to your console as resources are created.
3. Perform your tests/development
4. When you are done you can remove the stack using `cfn stack delete <path to deployment config>`