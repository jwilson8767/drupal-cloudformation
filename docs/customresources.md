Custom Resources
----------------
CloudFormation allows for extensibility via [custom resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-custom-resources.html). We use [Lambda-backed resources](https://aws.amazon.com/about-aws/whats-new/2015/04/aws-cloudformation-supports-aws-lambda-backed-custom-resources/) to define custom resource types which can be used and re-used in CloudFormation templates. For example, we create and manage mysql databases on pre-existing RDS Instances using Lambda functions.

Source code for each function can be found in `customresources/<function>/_src/code.py`
Logs are output to [CloudWatch](https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#logs:)

## Requirements

- Python 2.7+ (Python 3 is not yet supported by AWS Lambda)
- [AWS CLI](https://github.com/aws/aws-cli) - `pip install awscli` followed by `aws configure` to enter your default region (usually `us-east-1`) and your AWS access key
- [Kappa](https://github.com/garnaat/kappa) - `pip install kappa` (automated Lambda function deployment)

## Deploying changes
1. Update any `kappa.yml` files to match your desired AWS CLI profile (use `aws configure --profile <profile>` to add a new profile if needed.<!-- TODO After https://github.com/garnaat/kappa/pull/104 is merged, remove this step and update kappa.yml to use this as default.-->
2. Deploy your changes by either entering a specific lambda function's directory and using `./build.sh && kappa deploy` or deploying all lambda functions using `./customresources/deploy.sh`. **Your changes will immediately go into production, rename the function in `kappa.yml` for development/testing**

<span id="deploy-new-account"></span>
## Deploying on a new AWS Account
1. Create a new KMS key.
2. Update all kappa.yml files with the new KMS Key Arn.
3. Use `deploy-customresources.sh` to build and deploy all custom resources.

## Gotcha's
- Lambda functions inside a VPC only access AWS services which have an endpoint in that VPC. Currently S3 is the only AWS service to have an endpoint in every VPC by default. For this reason I recommend only creating Lambda functions outside VPCs. If they need to interact with resources inside a VPC, use security groups to allow them to do so.
- `kappa.yml` contains developer-specific values by design and requires customization before using Kappa.

## Further reading
AWS Lambda functions are incredibly powerful, but most of the most relevant documentation is buried, so here are some resources that may be helpful:
- [Extending CloudFormation with Lambda-Backed Custom Resources](https://blog.jayway.com/2015/07/04/extending-cloudformation-with-lambda-backed-custom-resources/)
- [Custom Resource - Request Types](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/crpg-ref-requesttypes.html)
- [Custom Resource - Making Requests](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/crpg-ref-requests.html)
- [Custom Resource - Sending Responses](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/crpg-ref-responses.html)
- [Lambda limits](https://docs.aws.amazon.com/lambda/latest/dg/limits.html)
- [Kappa config file reference](https://kappa.readthedocs.io/en/develop/config_file_example.html)
- [Kappa commands reference](https://kappa.readthedocs.io/en/develop/commands.html#deploy)
- [Boto3 documentation](https://boto3.readthedocs.io/en/latest/)
- [PyMySQL documentation](https://pymysql.readthedocs.io/en/latest/)
