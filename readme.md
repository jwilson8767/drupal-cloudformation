NEMAC Drupal CloudFormation
--------------------

This project provisions the resources required to deploy and manage Drupal in AWS. At a high level Drupal requires a webserver which supports PHP, a MySQL database, and store for images and other static assets. 

# Table of Contents

* [Background Information](#background)
  * [Infrastructure Overview](#infrastructure)
  * [Terms](#terms)
  * [Stack Types](#stack-types)
* [Usage](#usage)
  * [Starting a new Drupal project](#new-project)
  * [Deploying to a new Drupal environment](#deploy-new-environment)
  * [Merging changes](#merge-changes)
  * [Blue-Green deployment](#blue-green-deployment)
  * [Migrating an existing Drupal site](#migrate-site)
  * [Deleting stacks](#delete-stack)
* [Costs and Billing](#billing)
* [Development and Management](#develop-manage)
* [Gotchas](#gotchas)
* [General Troubleshooting](#troubleshooting)
  * Failure to deploy changes
  * HTTP 500
  * No-response (timeout)
  * Failure to deploy stack
  * Optimizing a large project
* [Futher Reading](#further-reading)

# <span id="background"></span>Background Information

**CloudFormation** is a tool used to manage AWS resources using parameterized template files. This allows non-technical users to setup and deploy applications into controlled, replicable, and disposable environment. When a template is deployed the resources it creates are collectively called a **stack**. Stacks can be created (new resources are provisioned for the first time), updated (existing resources are created, changed, swapped, or deleted as needed), and deleted at the click of a few buttons or commands. Mostly you will be interested in Project stacks and Environment stacks. (Note that each Project stack includes an Elastic Beanstalk Application and therefore when AWS refers to an "Application" they really are talking about our "Project" stack)

### <span id="infrastructure"></span>Infrastructure Overview
The diagram below illustrates the flow of requests, code, static assets, and data for a Drupal project. Notice that the MySQL instance and asset bucket are shared between projects in the same region.
![infrastructure diagram](docs/infrastructure-diagram.png)

### <span id="terms"></span>Terms
Term|Definition
:---|:---
**Resource** | Anything AWS can create or manage. For example: an S3 bucket, RDS instance, EC2 instance, or a Route53 recordset
**Project** | An application or website that is going to be deployed on AWS.
**Environment** | A single deployment of a single branch of a project.
**Stack** | A set of AWS resources created using a CloudFormation template.
**Change Set** | A preview of the changes that will result from updating a stack (not required to apply an update).


# <span id="stack-types"></span>Stack Types
| Name | Description | Cost |
|:---|:---|:---|
| <a target="_blank" href="https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=cfn-identities&templateURL=https://s3.amazonaws.com/nemac-cloudformation/master/templates/cfn-identities.yaml">**CloudFormation Identities**</a> | Sets up basic IAM Roles and Groups and a KMS key for this AWS Account. The very first stack to be created on any AWS Account. Be careful! Touching this can be dangerous! | --- |
| <a target="_blank" href="https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=cfn-region&templateURL=https://s3.amazonaws.com/nemac-cloudformation/master/templates/cfn-region.yaml">**CloudFormation Region**</a> | Provides buckets and network resources for this region's CloudFormation Drupal Stacks. Depends on `cfn-identities`. Ensure you set the IAM role to `cloudformation-role` during creation. If `cf-identities` already exists in another region, <a target="_blank" href="https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=cfn-region&templateURL=https://s3.amazonaws.com/nemac-cloudformation/master/templates/cfn-identities-secondary-region.yaml">create a `cf-identities-secondary-region` stack first</a>. | --- |
| <a target="_blank" href="https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=drupal-mysql56&templateURL=https://s3.amazonaws.com/nemac-cloudformation/master/templates/mysql-instance.yaml">**MySQL Instance**</a> | A MySQL RDS instance which can be used by other stacks. Depends on `cfn-region`.  Ensure you set the IAM role to `cloudformation-role` during creation. | [See RDS Instance Pricing](https://aws.amazon.com/rds/pricing/) |
| <a target="_blank" href="https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=someproject-com&templateURL=https://s3.amazonaws.com/nemac-cloudformation/master/templates/drupal-project.yaml">**Drupal Project**</a> | A ElasticBeanstalk-based Drupal project which can have many environments. Depends on `cfn-region`.  Ensure you set the IAM role to `cloudformation-role` during creation. | $1/mo
| <a target="_blank" href="https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=someproject-com-1&templateURL=https://s3.amazonaws.com/nemac-cloudformation/master/templates/drupal-environment.yaml">**Drupal Environment**</a> | An ElasticBeanstalk-based environment which supports automated deployment of Drupal projects. Depends on `cfn-region`, `drupal-project`, and `mysql-instance`. Ensure you set the IAM role to `cloudformation-role` during creation. | [See Costs and Billing](#billing) |

# <span id="usage"></span>Usage

### <span id="new-project"></span>Starting a new Drupal project
This requires you to be in the `cfn-developers` or `cfn-admins` IAM group. 

1. Create a new git repository on Github.
2. Clone the git repository to your development computer using the instructions provided by Github. ([Install Git](https://git-scm.com/downloads) if you haven't already)
3. Use `git remote add upstream https://github.com/jwilson8767/nemac-drupal-template.git` followed by `git pull upstream master`. During development you can push changes using `git push origin master`. I recommend also creating a production branch named "prod-v1" for your first deployment, subsequent breaking changes can be pushed to "prod-v2" then [Blue-Green deployed to avoid downtime](#blue-green-deployment).
4. You can now develop locally if you wish, see the readme in your project directory to learn how to setup your local development environment. 
5. When you're ready, continue to [Deploying to a new Drupal environment](#deploy-new-environment).

### <span id="deploy-new-environment"></span>Deploying to a new Drupal environment
1. Push your code to a production branch (Ex: "prod-v1") using `git push origin/prod-v1`.
2. <a target="_blank" href="https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=someproject-com&templateURL=https://s3.amazonaws.com/nemac-cloudformation/master/templates/drupal-project.yaml">Click here to create a new Drupal Project stack.</a>
    - Ensure you set the IAM role to `cloudformation-role`.
    - Check `I acknowledge that AWS CloudFormation might create IAM resources` at the bottom of the conformation page.
3. <a target="_blank" href="https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=someproject-com-1&templateURL=https://s3.amazonaws.com/nemac-cloudformation/master/templates/drupal-environment.yaml">Click here to create a new Drupal Environment stack.</a>
    - Enter your github information as needed, including generating a [personal access](https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/) token with `repo` access.
    - Ensure you enter the correct branch (for new projects this will be "master", but later on it will probably be "prod").
    - If this environment will *ever* go into production check `Retain Database` to ensure it is not accidentally cleaned up with the rest of the environment when it is deleted.
    - Ensure you set the IAM role to `cloudformation-role`.
    - Check `I acknowledge that AWS cloudformation might create IAM resources` at the bottom of the conformation page.
    - The environment will take a few minutes to provision and deploy, grab some coffee.
4. When the environment stack creation completes, copy the EB Hostname from the Outputs panel to your address bar, then add `/install.php` to begin the Drupal first-time setup. You will be asked to pick an email address the server should send from (usually something like `no-reply@someproject.com`) and to setup an admin account for yourself. 
5. All done! Your environment is now fully deployed. Any future changes pushed to the git branch this environment is watching will be deployed automatically within a few minutes. You can also change which branch this repo is following using the [CloudFormation Console](https://console.aws.amazon.com/cloudformation/) > this stack > `Update Stack`

### <span id="merge-changes"></span>Merging changes
See the nemac-drupal-project readme for merging changes from two environments/branches.

### <span id="blue-green-deployment"></span>Blue-Green Deployment
Blue-Green Deployment is a method of gradual deployment which allows you to ensure that a new release is ready and working without downtime. You can use it when you have major changes that need special care. For our purposes the "Blue" environment is the current production environment, and the "Green" environment is the new release.

1. Follow the guide for [Deploying to a new Drupal Environment](#deploy-new-environment), naming the stack something like "v2-somedomain-com" and the branch something like "prod-2.0", with the version number indicating a major release. Don't setup Route53/DNS just yet.
2. Once Green is provisioned and running, edit your computer's `hosts` file to point to the ip address of the Green environment, you can make changes as needed to get it ready for release. If HTTPS doesn't work, troubleshoot it now, not later.
3. Once you are satisfied that Green is ready, use the Route53 console to update the A record currently aliased to Blue's Elastic Beanstalk domain to now point to Green's Elastic Beanstalk domain. If something goes wrong, switch it back to make Blue active again.
4. Green should be active immediately, but DNS caching will prevent most devices from seeing Green for at least 2 hours. During that time they will still see Blue (this period is sometimes refered to as "draining"). I recommend keeping Blue around for 24 hours, or until you are sure that Green is stable and that Blue has been drained fully. Once you are satisfied, Blue may be deleted.

### <span id="migrate-site"></span>Migrating an existing site
You must be in the `cfn-admins` IAM group to complete this.

1. Identify the site’s directory on the existing server, database name, url, and git repository (create git repository if none exists presently)
2. Backup the site’s directory using `tar czf sitename.tgz sitedirectory`
3. Dump the site’s database using `sudo mysqldump --default-character-set=utf8 --databases sitedatabasename --protocol=tcp  --compress=TRUE --skip-extended-insert --dump-date=FALSE--skip-triggers --quick > sitename.sql`
4. Move the backup tar and sql files to your development machine. (using scp this would be something like `scp server:/path/to/sitename.tgz ./` on your local machine.)
5. Import the database to the active RDS MySQL instance:
    - Connect to the RDS instance's endpoint ([RDS Console](drrjrgarfcq13p.cj0oborxdlge.us-east-1.rds.amazonaws.com)) using your favorite MySQL client (MySQL Workbench works well)
    - Import the database that you exported in step 3 by running the script.
    - Note the database name as you will need it on step 10.
5. Untar the project source into a new project directory using `tar xzf sitename.tgz`.
6. Move the contents of `project/html/` to `newprojectdir/web/`. Delete the (now empty) `project/html` folder.
7. Pull the drupal project template files into the project directory using `git pull -X theirs https://github.com/jwilson8767/nemac-drupal-template.git`.
8. Commit all the files in the project directory to a new branch, push that branch to the project's GitHub repository.
9. <a target="_blank" href="https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=someproject-com&templateURL=https://s3.amazonaws.com/nemac-cloudformation/master/templates/drupal-project.yaml">Click here to create a new Drupal Project stack.</a>  Ensure you set the IAM role to `cloudformation-role`.
10. <a target="_blank" href="https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=someproject-com-1&templateURL=https://s3.amazonaws.com/nemac-cloudformation/master/templates/drupal-environment.yaml">Click here to create a new Drupal Environment stack.</a>
    - Enter your Github information as needed.
    - Make sure to enter the correct branch.
    - If this environment will go into production at any point check "Retain Database" to ensure it is not cleaned up with the rest of the environment when it is deleted.
    - You should generate a [personal access](https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/) token with `repo` access.
    - Ensure you set the IAM role to
     `cloudformation-role`.
   - Check I acknowledge that AWS cloudformation might create IAM resources.  (This is at the bottom of the confirmation page)
   - The environment will take a few minutes to spin up and deploy, grab some coffee.
11. Your environment should not be ready and functional. Connect to it using the link given in the output of the environment stack (or the Elastic Beanstalk console). Note that https is not yet implemented and that this section does not cover using Route53 to direct traffic to your environment.

### <span id="new-project"></span>Starting a new project
This requires you to be in the `cfn-developers` or `cfn-admins` IAM group.

1. [Install Git](https://git-scm.com/downloads) on the computer you will be developing with.
2. Create your new project:
    - Fork the [Drupal Project Template Github Repository](https://github.com/jwilson8767/nemac-drupal-template/)
    - Rename the repository to reflect the site or project
    - Clone your fork to your local machine using the instructions provided by Github. (optional if you do not need to make any code/theme changes at this time.)
3. <a target="_blank" href="https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=someproject-com&templateURL=https://s3.amazonaws.com/nemac-cloudformation/master/templates/drupal-project.yaml">Click here to create a new Drupal Project stack.</a>
    - Ensure you set the IAM role to `cloudformation-role`.
   - Check I acknowledge that AWS Cloudformation might create IAM resources.  (This is at the bottom of the confirmation page)
   - The environment will take a few minutes to spin up and deploy, grab some coffee.
11. Your environment should now be ready and functional. Connect to it using the link given in the output of the environment stack (or the Elastic Beanstalk console). Note that https is not yet implemented and that this section does not cover using Route53 to direct traffic to your environment.

### <span id="delete-stack"></span>Deleting stacks
To delete a stack, first delete dependant stacks, then use the `Delete Stack` button in the CloudFormation console.
 
 **If a deletion fails**: Note the resources that failed to delete (usually just one or two) by type and ids, remove each one manually using the relevant console, then re-attempt the deletion.
 
# <span id="develop-manage"></span>Development and Management

## <span id="dev-requirements"></span>Development/CLI usage Requirements

- [Git](https://git-scm.com/downloads)
- Python 2.7+ (Python 3 is not yet supported by AWS Lambda)
- [AWS CLI](https://github.com/aws/aws-cli) - `pip install awscli` followed by `aws configure` to enter your default region (usually `us-east-1`) and your AWS access key
- [Kappa](https://github.com/garnaat/kappa) - `pip install git+https://github.com/garnaat/kappa.git` (automated Lambda function deployment)
- [AWS CloudFormation CLI](https://github.com/Kotaimen/awscfncli) - `pip install awscfncli` (automated CloudFormation stack deployment)

## <span id="fresh-infrastructure"></span>Deploy on a fresh AWS Account
1. Create a new KMS key.
2. Update all `customresources/*/kappa.yml` files with the new KMS Key Arn.
3. Use `deploy-customresources.sh` to build and deploy all custom resources.
4. Run `deploy-templates.sh bucket-name` (bucket will be created if it doesn't already exist)
5. Verify that the bucket is created and populated, and that the lambda functions were created.
6. Deploy a <a target="_blank" href="https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=cfn-identities&templateURL=https://s3.amazonaws.com/nemac-cloudformation/master/templates/cfn-identities.yaml">CloudFormation Identities stack</a> using the new KMS key arn. (see "[deploying stacks via CLI](#deploy-via-cli)")
7. Deploy a <a target="_blank" href="https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=cfn-region&templateURL=https://s3.amazonaws.com/nemac-cloudformation/master/templates/cfn-region.yaml">Cloudformation Region stack</a> (making sure to use the newly created `cloudformation-role`).

At this point the account is ready for MySQL instances and Drupal Projects.

## <span id="deploy-via-cli"></span>Deploying stacks via CLI
1. Customize the appropriate example deployment config with values. (example files located in deployments directory)
2. Deploy using `cfn stack deploy <path to deployment config>`, the stack will be created and stack events will be printed out to your console as resources are created.
3. When you are done you can remove the stack using `cfn stack delete <path to deployment config>`

# <span id="troubleshooting"></span>General Troubleshooting
#### Failure to deploy changes from Github:
Login to the AWS Elastic Beanstalk Console, review the event log or download full logs to diagnose and resolve the issue, when your fixes are ready use the AWS CodePipeline console to "Release" which will re-run the deployment.
#### HTTP 500
Usually this is an application-level bug, so first check your Drupal configuration. Additionally, the AWS Elastic Beanstalk console will provide you with error logs that may be helpful.
#### No-response (timeout)
Verify the DNS entries are correct for the domain you are attempting to visit, then verify that the Elastic Beanstalk environment has a running instance, then review the logs for the environment.
#### HTTPS issues
<!-- TODO HTTPS troubleshooting docs -->
#### Failure to build new Elastic Beanstalk Environment from template
If a stack fails to deploy, first review its logs as often they will say exactly which resource failed. If the resource is in another stack, then troubleshoot that stack/resource directly, if it is part of the stack that failed to deploy then the issue may be in the parameters supplied when creating the new stack. Re-create the stack with corrected parameters. If that still doesn't work then troubleshoot the template directly to resolve issues with the specific resource that is failing.

## <span id="optimization"></span>Optimizing a large project
In order of estimated cost/complexity, low to high:
- Ensure all static asset links are directed to CloudFormation rather than going through the webserver. 
- Ensure Drupal's local caching is working properly.
- Setup a CloudFront distribution in front of Elastic Beanstalk to cache static pages.
- Switch to a larger instance by Updating the CloudFormation Stack's desired instance size.
- Move project's database to a larger/different RDS instance.
- It is possible to enable auto-scaling in Elastic Beanstalk, just be aware of the added cost of the Elastic Load Balancer.

# <span id="gotchas"></span>Gotchas
* While CloudFormation itself is very fast, each AWS resource will add its own creation time. Here are a few that add a notable delay:
    * RDS Instances create a full disk image upon creation, which can easily take 10 minutes even on small instances.
    * EC2 Instance Profiles wait exactly 2 minutes to allow for propagation.
    * EC2 instances can take 5+ minutes to spin up.
* Sometimes a failed creation or deletion will hang (especially if a resource is deleted outside of CloudFormation), but using `aws cloudformation delete-stack --stack-name NAME --retain-resources` will usually delete it immediately. If that doesn't work, wait 10 minutes and the stack will go to a "FAILED" status and should be able to be deleted using the command above.
* CodePipeline must be manually told to retry failed deployments or a new commit must be pushed.
* Elastic Beanstalk Environments are normally very stable, but in the event of an instance being terminated, it can take up to 10 minutes for a new instance to be fully provisioned. That said, sometimes the best way to get a failing environment back to stable is to terminate the offending instances and let EB start fresh on a new instance.
* Avoid the CloudFormation Designer, it's useless and creates buckets for no reason.

# Next steps for this project:
- Move this and nemac-drupal-project git repos to NEMAC repo.
- Setup an access token to NEMAC's GitHub organization, pass to codepipeline as default.
- Fully migrate an entire site.
- Use this project in a new project.

# <span id="further-reading"></span>Further reading
- The nemac-drupal-project readme
- [AWS CLI config reference](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html#cli-quick-configuration)
- [All CloudFormation Resource Types](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html)
- [CloudFormation built-in functions](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference.html)
- [CloudFormation built-in variables](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/pseudo-parameter-reference.html)
- [CloudFormation Resource Attributes](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-product-attribute-reference.html)
- [CloudFormation Outputs, Exports, and Cross-Stack references](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/outputs-section-structure.html)

