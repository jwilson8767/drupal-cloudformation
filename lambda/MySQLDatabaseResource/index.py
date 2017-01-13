from __future__ import print_function

"""
This is a CloudFormation Lambda-backed Custom Resource for MySQL Databases living inside RDS MySQL instances.
It handles common management tasks such as creating/cloning/removing schemas and creating/removing users.

Usage for testing:
  index.handler(json.loads('''
    {
        "ResourceProperties": {
            "KMSKeyARN": "",
            "Hostname": "",
            "Port": "3306",
            "Username": "",
            "Password": "",
            "Database": "",
            "RetainDatabase": "yes|no",
        },
        "RequestType": "Create|Update|Delete"
    }
'''),None)

Usage in a CloudFormation Template:
  "MySQLDatabase" : {
    "Type" : "AWS::CloudFormation::CustomResource",
    "Version" : "1.0",
    "Properties" : {
       "ServiceToken" : "This lambda function's ARN",
       "KMSKeyARN" : "",
       "Hostname" : "mysql.example",
       "Port" : "3306",
       "Username" : "",
       "password" : "",
       "Database" : "some-StackName"
       "RetainDatabase" : true
    }
  }
"""

import base64
import boto3
import cfnresponse
import pymysql
import pymysql.cursors
import random
import string

kmsKeyARN = None
kmsClient = boto3.client('kms')
connection = None


def handler(event, context):
    global connection, kmsKeyARN
    kmsKeyARN = event['ResourceProperties']['KMSKeyARN']
    print('connecting to mysql instance..')
    connection = pymysql.connect(host=event['ResourceProperties']['Hostname'],
                                 port=int(event['ResourceProperties']['Port']),
                                 user=decrypt(event['ResourceProperties']['Username']),
                                 password=decrypt(event['ResourceProperties']['Password']),
                                 cursorclass=pymysql.cursors.DictCursor)
    print('connected.')
    try:
        response = {}
        if event['RequestType'] == 'Create':
            response = create(event['ResourceProperties']['Database'])
        elif event['RequestType'] == 'Update':
            if event['ResourceProperties']['Database'] != event['OldResourceProperties']['Database']:
                update(event['ResourceProperties']['Database'], event['OldResourceProperties']['Database'])
        elif event['RequestType'] == 'Delete':
            if event['ResourceProperties']['RetainDatabase'] == 'no':
                delete(event['ResourceProperties']['Database'])
        else:
            print('invalid RequestType: ' + event['RequestType'])
        if context is not None:
            return cfnresponse.send(event, context, cfnresponse.SUCCESS, response, None)
    except:
        if context is not None:
            cfnresponse.send(event, context, cfnresponse.FAILED, {}, None)
        raise
    finally:
        print('closing connection')
        connection.close()


def create(database):
    """
    Create a new schema, a new user, and grant all to user on schema.
    :param database: string
    :return: {'encryptedUsername', 'encryptedPassword'}
    """
    username = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(12))
    password = ''.join(
        random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in
        range(15))
    print('generated username and password')
    with connection.cursor() as cursor:
        print('creating schema and user')
        cursor.execute("""
            CREATE SCHEMA IF NOT EXISTS {db} CHARACTER SET utf8 COLLATE utf8_general_ci;
            CREATE USER '{user}'@'%%' IDENTIFIED BY '{pass}';
            GRANT ALL PRIVILEGES ON {db}.* TO {user}@'%%';
            """.format(**{
            'db': connection.escape_string(database),
            'user': connection.escape_string(username),
            'pass': connection.escape_string(password)
        }), ())
    connection.commit()
    return {
        'encryptedUsername': encrypt(username),
        'encryptedPassword': encrypt(password)
    }


def update(database, olddatabase):
    """
    Database name has been changed, create it if it doesn't already exist, and grant privileges to it.
    :param database: string
    :param olddatabase:  string
    :return:
    """
    print('Updating schema and user')
    with connection.cursor() as cursor:
        cursor.execute("""
                CREATE SCHEMA IF NOT EXISTS {db} CHARACTER SET utf8 COLLATE utf8_general_ci;
                UPDATE mysql.db SET Db = '{db}' WHERE Db='{olddb}';
                """.format(**{
            'db': connection.escape_string(database),
            'olddb': connection.escape_string(olddatabase)
        }), ())
    connection.commit()


def delete(database):
    """
    Delete the existing schema, revoke database-level privileges, and drop user.
    :param database: string
    :return:
    """
    with connection.cursor() as cursor:
        print('dropping schema and user')
        cursor.execute("""
                SELECT @user:=User, @host:=Host FROM mysql.db WHERE Db = '{db}';
                DELETE FROM mysql.db WHERE Db = '{db}' AND User = @user;
                DELETE FROM mysql.user WHERE user=@user AND host=@Host;
                DROP DATABASE {db};
            """.format(**{
            'db': connection.escape_string(database)
        }), ())
    connection.commit()


def encrypt(value):
    """
    Encrypts a value using AWS KMS
    :param value: string
    :return: string
    """
    r = kmsClient.encrypt(KeyId=kmsKeyARN, Plaintext=value)
    if 'CiphertextBlob' in r:
        return base64.b64encode(r['CiphertextBlob'])
    else:
        print('Invalid response from kms during encrypt:')
        print(r)
        exit()


def decrypt(value):
    """
    Decrypts a value using AWS KMS
    :type value: string
    """
    r = kmsClient.decrypt(CiphertextBlob=base64.b64decode(value))

    if 'Plaintext' in r:
        return r['Plaintext']
    else:
        print('Invalid response from kms during decrypt:')
        print(r)
        exit()
