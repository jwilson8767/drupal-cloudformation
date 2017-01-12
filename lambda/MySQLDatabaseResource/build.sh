#!/usr/bin/env bash
#Installs, then packages the virtualenv's packages and this project's source for use by AWS Lambda
pip install virtualenv

virtualenv ./

source ./bin/activate

pip install pymysql

rm -rf MySQLDatabaseResource.zip

pushd ./lib/python2.7/site-packages
zip  -r9 $OLDPWD/MySQLDatabaseResource.zip . --exclude pip\* --exclude setuptools\* --exclude virtualenv\* --exclude easy_install*
popd

zip -r9J ./MySQLDatabaseResource.zip ./*.py