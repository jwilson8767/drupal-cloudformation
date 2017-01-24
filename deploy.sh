#!/usr/bin/env bash
#uses the AWS CLI to upload templates and lambda function bundles
pushd $( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
for i in *.yaml; do
echo validating $i
(aws cloudformation validate-template --template-body file://$i &&  aws s3 cp "$i" s3://nemac-cloudformation/) | grep 'error\|upload'
done;
popd

