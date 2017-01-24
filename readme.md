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

### <a target="_blank" href="https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=cf-identities&templateURL=https://s3.amazonaws.com/nemac-cloudformation/cf-identities.yaml">CloudFormation Identities</a>
Sets up basic IAM Roles and Groups and a KMS key for this AWS Account. The very first stack to be created on any AWS Account. Don't mess with this unless you know what you're doing.
### <a target="_blank" href="https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=cf-region&templateURL=https://s3.amazonaws.com/nemac-cloudformation/cf-region.yaml">Drupal Region</a>
Provides buckets and network resources for this region's CloudFormation Drupal Stacks. Depends on `cf-identities`.
### <a target="_blank" href="https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=drupal-mysql56&templateURL=https://s3.amazonaws.com/nemac-cloudformation/mysql-instance.yaml">MySQL Instance</a>
A MySQL RDS instance which can be used by other stacks. Depends on `cf-region`.
### <a target="_blank" href="https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=someproject-com&templateURL=https://s3.amazonaws.com/nemac-cloudformation/drupal-application.yaml">Drupal Application</a>
A ElasticBeanstalk-based Drupal application which can have many environments. Depends on `cf-region`.
### <a target="_blank" href="https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=someproject-com-1&templateURL=https://s3.amazonaws.com/nemac-cloudformation/drupal-environment.yaml">Drupal Environment</a>
A ElasticBeanstalk-based environment which supports automated deployment of Drupal projects. Depends on `cf-region`, `drupal-application`, and `mysql-instance`
## Creating a new application
Before an CloudFormation application is created the project should already have a non-empty git repository. Additionally a MySQL Instance stack should be created

## Updating an application
## Deleting an application

## Troubleshooting
<!-- TODO Write troubleshooting -->
## CloudFormation Gotcha's
* !ImportValue works fine if given a string, but for substitutions (!Sub) you must use the long format. Ex: {'Fn::ImportValue': !Sub 'example-${AWS::StackName}'} to
* Sometimes a failed creation or deletion will hang (especially if a resource is deleted outside of CloudFormation), but using `aws cloudformation delete-stack --stack-name NAME --retain-resources` will usually delete it immediately. If that doesn't work, wait 10 minutes and the stack will go to a "FAILED" status and should be able to be deleted using the command above.

<!-- TODO Write a meaningful contributing guide -->