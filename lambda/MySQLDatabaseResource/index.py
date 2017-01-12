###
#  This is a CloudFormation Lambda-backed Custom Resource for MySQL Databases living inside RDS MySQL instances.
#  It handles common management tasks such as creating/cloning/removing schemas and creating/removing users.
#
#  Usage:
#    "MySQLDatabase" : {
#      "Type" : "AWS::CloudFormation::CustomResource",
#      "Version" : "1.0",
#      "Properties" : {
#         "ServiceToken" : "This lambda function's ARN",
#         "KMSKeyARN" : "",
#         "Hostname" : "mysql.example",
#         "Port" : "3306",
#         "AdminUsername" : "root",
#         "AdminPassword" : "1234",
#         "Database" : "some-stack-name"
#         "RetainDatabase" : true
#         "CloneSourceDatabaseName" : "old-stack-name"
#         "CloneSourceHostname" : "old.mysql.example"
#         "CloneSourcePort" : "3306"
#         "CloneSourceAdminUsername" : "root"
#         "CloneSourceAdminPassword" : "1234"
#      }
#    },
###

import base64
import boto3
import cfnresponse
import pymysql
import random
import string

kmsClient = boto3.client('kms')
kmsKeyARN = ''


def handler(event, context):
    global kmsKeyARN
    kmsKeyARN = event['ResourceProperties']['KMSKeyARN']
    print 'connecting to mysql instance..'
    connection = pymysql.Connect(host=event['ResourceProperties']['Hostname'],
                                 port=event['ResourceProperties']['Port'],
                                 user=decrypt(event['ResourceProperties']['Username']),
                                 password=decrypt(event['ResourceProperties']['Password']),
                                 cursorclass=pymysql.cursors.DictCursor)
    print 'connected.'
    if event['RequestType'] == 'Create':
        # TODO implement cloning functionality
        # Create a new schema, a new user, and grant all to user on schema.
        username = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(12))
        password = ''.join(
            random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in
            range(16))
        print 'generated username and password'
        print username
        print password
        with connection.cursor() as cursor:
            print 'creating schema and user'
            cursor.execute("""
                CREATE SCHEMA IF NOT EXISTS `%s` DEFAULT CHARACTER SET `utf8`;
                CREATE USER `%s`@`%` IDENTIFIED BY '%s';
                GRANT ALL PRIVILEGES ON `%s`.* TO `%s`@`%`;
            """, (event['ResourceProperties']['stack-name'], username, password, event['ResourceProperties']['stack-name'],
                  username))
        connection.commit()
        return cfnresponse.send(event, context, cfnresponse.SUCCESS, {
            'encryptedUsername': encrypt(username),
            'encryptedPassword': encrypt(password)
        }, {})
    elif event['RequestType'] == 'Update':
        return cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
    elif event['RequestType'] == 'Delete':
        if event['ResourceProperties']['RetainDatabase'] == 'yes':
            return cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
        # Delete the existing schema, revoke database-level privileges, and drop user.
        with connection.cursor() as cursor:
            print 'dropping schema and user'
            cursor.execute("""
                SELECT @user:=User, @host:=Host FROM mysql.db WHERE Db = '%s';
                DELETE FROM mysql.db WHERE Db = '%s';
                DELETE FROM mysql.user WHERE user=@user AND host=@Host;
            """, (event['ResourceProperties']['stack-name'], event['ResourceProperties']['stack-name']))
        connection.commit()
        return cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
    print 'closing connection'
    connection.close()


def encrypt(value):
    global kmsKeyARN, kmsClient
    return base64.b64encode(kmsClient.encrypt(KeyId=kmsKeyARN, Plaintext=kmsClient.encrypt(value))['CiphertextBlob'])


def decrypt(value):
    return kmsClient.decrypt(CiphertextBlob=base64.b64decode(value))
