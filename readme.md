## Concepts
### CloudFormation
CloudFormation is a tool used to manage AWS resources using parameterized template files. This allows non-technical users to setup pre-defined applications, environments, and deployments in a controlled, replicable, and disposable manner. When a template is used the resources it creates are collectively called a **stack**. Because resources can depend on other resource, sometimes it's important to define multiple stacks for a single application. Stacks can be created (new resources are provisioned for the first time), updated (existing resources are created, changed, swapped, or deleted), and deleted (all resources are deleted) by users with minimal IAM permissions. Templates are version controlled, so even as templates change an CloudFormation admin can always recreate an old stack if needed.

## Terms
Term|Definition
---|---
**Resource**|Anything AWS can create or manage. For example: an S3 bucket, an RDS instance, and EC2 instance, or a Route53 recordset
**Application**|A project or website that is going to be deployed on AWS.
**Environment**|A single deployment of a single branch of an application.
**Stack**|A set of AWS resources created using a CloudFormation template.
**Change Set**|A preview of the changes that will result from updating a stack.

## Stacks
### CloudFormation VPC
A VPC specifically for resources created by CloudFormation. Prevents interaction between CF stacks and pre-existing resources.
### Artifact Store
A private S3 bucket which can be used by other stacks for CodePipeline and Elastic Beanstalk artifact storage.
### Asset Store
A public S3 bucket which can serve static assets for other stacks.
### MySQL Instance
A MySQL RDS instance which can be used by other stacks.
### Drupal Application
A ElasticBeanstalk-based Drupal application which can have many environments.
### Drupal Environment
A ElasticBeanstalk-based environment which supports automated deployment of Drupal projects.
## Creating a new application
Before an CloudFormation application is created the project should already have a non-empty git repository. Additionally a MySQL Instance stack should be created

## Updating an application
## Deleting an application

##Troubleshooting


