#!/usr/bin/env bash
# Use this to get a new AWS account or region ready for nemac-cloudformation templates.
# It will create service roles for CloudFormation, a private bucket for
# templates to live in, and will create a VPC stack for use by other stacks later.

# Note: you will need to have the AWS CLI installed and configured with an access key to use this script.
# Use `aws configure` to update the default region to the region you would like to provision.

aws iam create-role --role-name cf-service-role --cli-input-json file://cf-service-role.json
aws iam create-role --role-name cf-codepipeline-role --cli-input-json file://cf-codepipeline-role.json
aws iam create-role --role-name cf-elasticbeanstalk-role --cli-input-json file://cf-elasticbeanstalk-role.json

aws s3 mb s3://nemac-cloudformation/

#TODO write other first-run steps