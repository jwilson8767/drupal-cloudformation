#!/usr/bin/env bash
# Use this to get a new AWS account ready for nemac-cloudformation templates.
# It will create service roles for CloudFormation and a private bucket for
# templates to live in.

# Requirements:
# - AWS CLI installed and configured with an access key to use this script.
# - python 2.7
# - Kappa (pip install kappa)

echo "creating template bucket if it doesn't exist..."
aws s3 mb s3://nemac-cloudformation/

echo "deploying custom resources"
pushd ./customresources/
templates/deploy.sh
popd

echo 'validating and uploading templates...'
pushd ./templates
templates/deploy.sh
popd
echo 'creating CloudFormation Identities stack...'
cfn stack deploy deployments/cf-identities.yaml