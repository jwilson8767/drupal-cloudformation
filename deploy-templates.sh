#!/usr/bin/env bash
# Uses the AWS CLI to upload templates to S3. Provided a specific file
#
# Usage:
#   deploy bucket-name [file]
# If file is omitted, then all will be deployed.
#
if [ -z "$1" ]; then
    bucket="nemac-cloudformation"
fi

aws s3 mb s3://${bucket}

pushd $( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

branch=$(git symbolic-ref --short -q HEAD)
if [ -z "$branch" ]; then
    echo "Not on a branch, exiting."
    exit 1
fi
if [ -z "$2" ]; then
        pushd ./templates
            for i in *.yaml; do
                echo validating $i
                (aws cloudformation validate-template --template-body file://$i &&  aws s3 cp "$i" s3://${bucket}/${branch}/templates/) | grep 'error\|upload'
            done;
        popd
    else
        i=$2
        echo validating $i
        aws cloudformation validate-template --template-body file://$i
        if [ $? -ne 0 ]; then
            echo "Failed validation test, exiting."
            exit 1
        fi
        aws s3 cp "$i" s3://${bucket}/${branch}/templates/
        if [ $? -ne 0 ]; then
            echo "Failed upload, exiting."
            exit 1
        fi
    fi
popd

