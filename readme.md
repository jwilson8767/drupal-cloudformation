## CloudFormation
CloudFormation is a tool used to manage AWS resources using parameterized template files. This allows non-technical users to setup pre-defined applications, environments, and deployments in a controlled, replicable, and disposable manner. When a template is used the resources it creates are collectively called a **stack**. Because resources can depend on other resources, sometimes it's important to define multiple stacks for a single application. Stacks can be created (new resources are provisioned for the first time), updated (existing resources are created, changed, swapped, or deleted), and deleted by users with permissions. Templates are version controlled, which makes it easy to track and manage configuration changes over time.

## Terms
Term|Definition
---|---
**Resource**|Anything AWS can create or manage. For example: an S3 bucket, an RDS instance, and EC2 instance, or a Route53 recordset
**Application**|A project or website that is going to be deployed on AWS.
**Environment**|A single deployment of a single branch of an application.
**Stack**|A set of AWS resources created using a CloudFormation template.
**Change Set**|A preview of the changes that will result from updating a stack.

## Stack Types

### <a target="_blank" href="https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=drupal-artifacts&templateURL=https://s3.amazonaws.com/nemac-cloudformation/CloudFormationVPC.yaml">CloudFormation VPC</a>
A VPC specifically for resources created by CloudFormation. Prevents interaction between CF stacks and pre-existing resources.
### <a target="_blank" href="https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=drupal-artifacts&templateURL=https://s3.amazonaws.com/nemac-cloudformation/ArtifactStore.yaml">Artifact Store</a>
A private S3 bucket which can be used by other stacks for CodePipeline and Elastic Beanstalk artifact storage.
### <a target="_blank" href="https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=drupal-assets&templateURL=https://s3.amazonaws.com/nemac-cloudformation/AssetStore.yaml">Asset Store</a>
A public S3 bucket which can serve static assets for other stacks.
### <a target="_blank" href="https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=drupal-mysql56&templateURL=https://s3.amazonaws.com/nemac-cloudformation/MySQLInstance.yaml">MySQL Instance</a>
A MySQL RDS instance which can be used by other stacks.
### <a target="_blank" href="https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=someproject-com&templateURL=https://s3.amazonaws.com/nemac-cloudformation/DrupalApplication.yaml">Drupal Application</a>
A ElasticBeanstalk-based Drupal application which can have many environments.
### <a target="_blank" href="https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=someproject-com-1&templateURL=https://s3.amazonaws.com/nemac-cloudformation/DrupalEnvironment.yaml">Drupal Environment</a>
A ElasticBeanstalk-based environment which supports automated deployment of Drupal projects.
## Creating a new application
Before an CloudFormation application is created the project should already have a non-empty git repository. Additionally a MySQL Instance stack should be created

## Updating an application
## Deleting an application

## Troubleshooting
<!-- TODO Write troubleshooting -->
## CloudFormation Gotcha's
* !ImportValue works fine if given a string, but for substitutions (!Sub) you must use the long format. Ex: {'Fn::ImportValue': !Sub 'example-${AWS::StackName}'} to
* Sometimes a failed creation or deletion will hang (especially if a resource is deleted outside of CloudFormation), but using `aws cloudformation delete-stack --stack-name NAME --retain-resources` will usually delete it immediately. If that doesn't work, wait ~15min and the stack will go into "_FAILED" mode and should be able to be deleted.

## Contributing
CloudFormation is a very powerful tool, but ultimately it still needs someone who understands the underlying resources to use it effectively.
<!-- TODO Write a meaningful contributing guide -->