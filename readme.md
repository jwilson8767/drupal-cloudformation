
NEMAC CloudFormation
--------------------

**CloudFormation** is a tool used to manage AWS resources using parameterized template files. This allows non-technical users to setup and deploy applications into controlled, replicable, and disposable environment. When a template is deployed the resources it creates are collectively called a **stack**. Stacks can be created (new resources are provisioned for the first time), updated (existing resources are created, changed, swapped, or deleted as needed), and deleted at the click of a few buttons or commands. Mostly you will be interested in Project stacks and Environment stacks. (Note that each Project stack includes an Elastic Beanstalk Application and therefore when AWS refers to an "Application" they really are talking about our "Project" stack)

See also: [Admin Documentation](documentation/readme.md)

## <a name="create-project"></a>Starting a new project
Do this if you have a new Drupal project that you want to design/develop/deploy.

1. Get your environment ready:
    - [Install Git](https://git-scm.com/downloads) on the computer you will be developing with.
    - (optional) [Install the AWS CLI](https://aws.amazon.com/cli/), [generate your access key](), and use `aws configure` to enter your access key to make it easier to manage stacks later on.
2. Create your new project:
    - Create a GitHub repository for your project.
    - `git remote add <Repository URL>` followed by `git push origin master`
    - Copy the template project files into your project directory using `git archive --format=tar --remote=<repository URL> HEAD | tar xf -`
3. Click here to create a new Drupal Project stack: <a target="_blank" href="https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=someproject-com&templateURL=https://s3.amazonaws.com/nemac-cloudformation/drupal-project.yaml"><img src="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png" alt="Launch Stack"/></a>
4. Click here to create a new Drupal Environment stack:  <a target="_blank" href="https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=someproject-com-1&templateURL=https://s3.amazonaws.com/nemac-cloudformation/drupal-environment.yaml"><img src="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png" alt="Launch Stack" _/></a>
5. Login to your drupal environment using the default login.


## <a name="clone-production"></a>Cloning the production environment to ~~avoid breaking stuff~~ develop in a safe environment.
Do this if you have a branch you want to experiment with, test new updates to Drupal, or just develop in your own space without disrupting the production environment. Later you can either commit your changes to the master branch of the project's github repository(at which point the changes will be automatically deployed to the production environment) or [assign your new environment as the production environment for the Application stack](#replace-production-environment).

## <a name="delete-environment"></a>Deleting stacks
Deleting a stack is usually super easy: Just use the `Delete Stack` button in CloudFormation. If that fails, you may have to delete dependant stacks first. For example, before you can delete an Application stack, you have to delete all of the Environment stacks that depend on it. If a deletion fails, you can try using `aws cloudformation delete-stack --stack-name "<Stack Name>" --retain-resources`, but then you will have to manually clean up all of the resources left behind.

## <a name="assign-production-environment"></a>Assigning a production environment

## <a name="replace-production-environment"></a>Replacing a production environment

## <a name="troubleshooting"></a>Troubleshooting
Some jerk didn't write any tips for you. I guess you're screwed. <!--TODO write troubleshooting -->





