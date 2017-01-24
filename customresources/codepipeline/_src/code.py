from __future__ import print_function
import boto3
import cfnresponse


def handler(event, context):
    args = {
        "pipeline": event['ResourceProperties']['PipelineName'],
        "token": event['ResourceProperties']['OAuthToken'],
        "owner": str(event['ResourceProperties'][:'Repository'])[str(event['ResourceProperties']['Repository']).index('/')],
        "repo": str(event['ResourceProperties']['Repository'])[str(event['ResourceProperties']['Repository']).index('/') + 1:],
        "branch": event['ResourceProperties']['Branch'],
        "environment": event['ResourceProperties']['Environment']
    }
    if event['RequestType'] == 'Create':
        create(**args)
    elif event['RequestType'] == 'Update':
        update(**args)
    elif event['RequestType'] == 'Delete':
        delete(**args)
    return cfnresponse.send(event, context, cfnresponse.SUCCESS)


def create(pipeline, token, owner, repo, branch, application, environment):
    client = boto3.client('codepipeline')
    config = client.get_pipeline(
        name=pipeline,
        version=1
    )
    config['pipeline']['stages'][0]['actions'].push({
        "outputArtifacts": [
            {"name": environment}
        ],
        "inputArtifacts": [],
        "name": environment,
        "configuration": {
            "Repo": repo,
            "OAuthToken": "****",
            "Owner": owner,
            "Branch": branch
        },
        "runOrder": 1,
        "actionTypeId": {
            "provider": "GitHub",
            "owner": "ThirdParty",
            "version": "1",
            "category": "Source"
        }
    })

    config['pipeline']['stages'][1]['actions']({
        "runOrder": 1,
        "configuration": {
            "EnvironmentName": environment,
            "ApplicationName": application
        },
        "outputArtifacts": [],
        "name": environment,
        "actionTypeId": {
            "owner": "AWS",
            "version": "1",
            "category": "Deploy",
            "provider": "ElasticBeanstalk"
        },
        "inputArtifacts": [
            {
                "name": environment
            }
        ]
    })


def update(pipeline, token, old, new):
    return


def delete(pipeline, token, environment):
    return


def dummy_actions(config):
    """Adds/Removes dummy actions as needed to comply with CodePipeline's requirement
     that each pipeline must have at least one source and one deploy action."""
    if len(config['pipeline']['stages'][0]['Actions']) == 0:
        config['pipeline']['stages'][0]['Actions'] += {
            "runOrder": 1,
            "actionTypeId": {
                "category": "Source",
                "version": "1",
                "provider": "S3",
                "owner": "AWS"
            },
            "inputArtifacts": [],
            "outputArtifacts": [
                {
                    "name": "dummyApp"
                }
            ],
            "configuration": {
                "S3Bucket": "dummybucket",
                "S3ObjectKey": "dummyobject.zip"
            },
            "name": "dummysource"
        }
    elif len(config['pipeline']['stages'][0]['Actions']) > 1:
        config['pipeline']['stages'][0]['Actions'][:] = [x for x in config['pipeline']['stages'][0]['Actions'] if
                                                         not x['name'] == 'dummysource']

    if len(config['pipeline']['stages'][1]['Actions']) == 0:
        config['pipeline']['stages'][1]['Actions'] += {
            "runOrder": 1,
            "actionTypeId": {
                "category": "Deploy",
                "version": "1",
                "provider": "CloudFormation",
                "owner": "AWS"
            },
            "inputArtifacts": [
                {
                    "name": "dummyApp"
                }
            ],
            "outputArtifacts": [],
            "configuration": {
                "ActionMode": "CREATE_UPDATE",
                "TemplatePath": "MyApp::a.json",
                "RoleArn": "arn:aws:iam::104538610210:role/nemac-cloudformation-role",
                "TemplateConfiguration": "MyApp::asdf.json",
                "StackName": "drupal-artifacts"
            },
            "name": "dummydeploy"
        }
    elif len(config['pipeline']['stages'][1]['Actions']) > 1:
        config['pipeline']['stages'][1]['Actions'][:] = [x for x in config['pipeline']['stages'][1]['Actions'] if
                                                         not x['name'] == 'dummydeploy']

    return config
