from __future__ import print_function
import boto3
import cfnresponse
import logging


def handler(event, context):
    try:
        print('checking args..')
        args = {
            "application": event['ResourceProperties']['Application'],
            "token": event['ResourceProperties']['OAuthToken'],
            "owner": str(event['ResourceProperties']['Repository'])[:str(event['ResourceProperties']['Repository']).index('/')],
            "repo": str(event['ResourceProperties']['Repository'])[
                    str(event['ResourceProperties']['Repository']).index('/') + 1:],
            "branch": event['ResourceProperties']['Branch'],
            "environment": event['ResourceProperties']['Environment']
        }
        client = boto3.client('codepipeline')
        pipeline = client.get_pipeline(name=args['application'])['pipeline']
        if event['RequestType'] == 'Create':
            print('creating pipeline')
            pipeline = create(pipeline, **args)
        elif event['RequestType'] == 'Update':
            print('removing old pipeline')
            pipeline = delete(pipeline,event['OldResourceProperties']['Environment'])
            pipeline = create(pipeline, **args)
        elif event['RequestType'] == 'Delete':
            print('deleting pipeline')
            pipeline = delete(pipeline, args['environment'])

        pipeline = dummy_actions(pipeline)
        client.update_pipeline(pipeline=pipeline)
        cfnresponse.send(event, context, cfnresponse.SUCCESS)
    except:
        logging.exception("Unhandled Exception")
        cfnresponse.send(event, context, cfnresponse.FAILED)
        raise


def create(pipeline, application, token, owner, repo, branch, environment):
    pipeline['stages'][0]['actions'].append({
        "name": environment,
        "outputArtifacts": [
            {"name": environment}
        ],
        "inputArtifacts": [],
        "configuration": {
            "Repo": repo,
            "OAuthToken": token,
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
    pipeline['stages'][1]['actions'].append({
        "name": environment,
        "runOrder": 1,
        "configuration": {
            "EnvironmentName": environment,
            "ApplicationName": application
        },
        "outputArtifacts": [],
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
    return pipeline


def delete(pipeline, environment):
    stages = []
    for stage in  pipeline['stages']:
        actions = []
        for action in stage['actions']:
            if action['name'] != environment:
                actions.append(action)
        stage['actions'] = actions
        stages.append(stage)
    pipeline['stages'] = stages
    return pipeline


def dummy_actions(pipeline):
    """Adds/Removes dummy actions as needed to comply with CodePipeline's requirement
     that each pipeline must have at least one source and one deploy action."""
    if len(pipeline['stages'][0]['actions']) == 0 or len(pipeline['stages'][1]['actions']) == 0:
        pipeline['stages'][0]['actions'].append({
            "name": "dummy",
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
            }
        })
        pipeline['stages'][1]['actions'].append({
            "name": "dummy",
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
                "StackName": "dummy"
            }
        })
    elif len(pipeline['stages'][0]['actions']) > 1 and len(pipeline['stages'][1]['actions']) > 1:
        pipeline = delete(pipeline, 'dummy')
    return pipeline
