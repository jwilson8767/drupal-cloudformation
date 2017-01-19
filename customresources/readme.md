CloudFormation allows for extensibility via [custom resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-custom-resources.html). We use [Lambda-backed resources](https://aws.amazon.com/about-aws/whats-new/2015/04/aws-cloudformation-supports-aws-lambda-backed-custom-resources/) to define custom resource types which can be used and re-used in CloudFormation templates.

## Development
To get started, just [install Gordon](https://gordon.readthedocs.io/en/latest/installation.html) (`pip install gordon`) and have at! Use `gordon build` to build, `cat tests/$lambda.json | gordon run $lambda.lambda` to test gordon locally, and `gordon apply` to deploy these custom resource types.

### Gordon
[Gordon](https://github.com/jorgebastida/gordon) provides dependency management (with the help of pip-formatted `requirements.txt` files), automated building (`gordon build`), basic testing, and automated deployment (using CloudFormation!) for our custom resources.

### cfnresponse
This python module provides an easy way to send responses to CloudFormation `Create`, `Update`, and `Delete` events.

### Building

### Testing

### Deployment