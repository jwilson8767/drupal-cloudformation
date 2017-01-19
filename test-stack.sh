#!/usr/bin/env bash
echo validating template...
aws cloudformation validate-template --template-body file://$1

#TODO write a proper testing script (integration testing?)