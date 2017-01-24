#!/usr/bin/env bash
#uses the AWS CLI to upload templates
for i in *.yaml; do
aws cloudformation validate-template --template-body file://$i & aws s3 cp "$i" s3://nemac-cloudformation/;
done;
