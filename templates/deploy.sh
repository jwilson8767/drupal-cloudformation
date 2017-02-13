#!/usr/bin/env bash
# Uses the AWS CLI to upload templates to S3.
#
# Usage:
#   deploy [file]


pushd $( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

branch=$(git symbolic-ref --short -q HEAD)
if [ -z "$branch" ]
then
    echo "Not on a branch, exiting."
    exit 1
fi

if [ -z "$1" ]
    then
        for i in *.yaml
        do
        echo validating $i
        (aws cloudformation validate-template --template-body file://$i &&  aws s3 cp "$i" s3://nemac-cloudformation/${branch}/) | grep 'error\|upload'
        done;
    else
        i=$1
        echo validating $i
        aws cloudformation validate-template --template-body file://$i
        if [ $? -ne 0 ]
        then
            echo "Failed validation test, exiting."
            exit 1
        fi
        aws s3 cp "$i" s3://nemac-cloudformation/${branch}/
        if [ $? -ne 0 ]
        then
            echo "Failed upload, exiting."
            exit 1
        fi
    fi
popd

