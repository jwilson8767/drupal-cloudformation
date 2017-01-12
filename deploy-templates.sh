#!/usr/bin/env bash
#uses the AWS CLI to upload templates
target="s3://nemac-cloudformation/"
aws s3 cp CloudFormationVPC.template $target
aws s3 cp DrupalApp.template $target
aws s3 cp DrupalEnvironment.template $target
aws s3 cp MySQLInstance.template $target
aws s3 cp AssetStore.template $target
aws s3 cp ArtifactStore.template $target