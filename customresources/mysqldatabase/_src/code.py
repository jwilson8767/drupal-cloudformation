from __future__ import print_function

import base64
import boto3
import cfnresponse
import pymysql
import pymysql.cursors
import random
import string
import logging

kmsClient = boto3.client('kms')
connection = None

kmsKeyARN = None
application = None


def handler(event, context):
    global connection, kmsKeyARN, application
    try:
        print(event)
        kmsKeyARN = event['ResourceProperties']['KMSKeyARN']
        application = event['ResourceProperties']['Application']
        print('Connecting to mysql instance..')
        connection = pymysql.connect(host=event['ResourceProperties']['Hostname'],
                                     port=int(event['ResourceProperties']['Port']),
                                     user=event['ResourceProperties']['Username'],
                                     password=decrypt(event['ResourceProperties']['Password']),
                                     cursorclass=pymysql.cursors.DictCursor)
        print('Connected.')
        response = {}
        if event['RequestType'] == 'Create':
            response = create(database=event['ResourceProperties']['Database'])
        elif event['RequestType'] == 'Update':
            response = update(database=event['ResourceProperties']['Database'],
                              old_database=event['OldResourceProperties']['Database'], username=event['PhysicalResourceId'])
        elif event['RequestType'] == 'Delete':
            if event['ResourceProperties']['RetainDatabase'] == 'no':
                delete(database=event['ResourceProperties']['Database'], username=event['PhysicalResourceId'])
            else:
                print('Retaining Database.')
        else:
            print('Invalid RequestType: ' + event['RequestType'])

        return cfnresponse.send(event,
                                context,
                                cfnresponse.SUCCESS,
                                response_data=response,
                                physical_resource_id=(
                                response['PhysicalResourceId'] if 'PhysicalResourceId' in response else None))
    except:
        logging.exception("Unhandled Exception")
        cfnresponse.send(event, context, cfnresponse.FAILED)
    finally:
        print('closing connection.')
        connection.close()


def create(database):
    """
    Create a new schema, a new user, and grant all to user on schema.
    :param database: string
    :return: {'username', 'encryptedPassword'}
    """
    username = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(12))
    password = ''.join(
        random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in
        range(15))
    print('generated new username and password')
    with connection.cursor() as cursor:
        print('Creating schema and user...')
        cursor.execute("""
            CREATE SCHEMA IF NOT EXISTS `{db}` CHARACTER SET utf8 COLLATE utf8_general_ci;
            CREATE USER '{user}'@'%%' IDENTIFIED BY '{pass}';
            GRANT ALL PRIVILEGES ON `{db}`.* TO '{user}'@'%%';
            """.format(**{
            'db': connection.escape_string(database),
            'user': connection.escape_string(username),
            'pass': connection.escape_string(password)
        }), ())
    connection.commit()
    print('Create complete.')
    return {
        'PhysicalResourceId': username,
        'Username': username,
        'EncryptedPassword': encrypt(password, database)
    }


def update(database, old_database, username):
    """
    Database name has been changed, create it if it doesn't already exist, and grant privileges to it.
    :param database: string
    :param old_database:  string
    :return:
    """
    password = ''.join(
        random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in
        range(15))
    print('generated new password')
    print('Updating schema and user...')
    with connection.cursor() as cursor:
        cursor.execute("""
                CREATE SCHEMA IF NOT EXISTS `{db}` CHARACTER SET utf8 COLLATE utf8_general_ci;
                UPDATE mysql.db SET Db = '{db}' WHERE Db='{olddb}' AND User = '{user}';
                SET PASSWORD FOR '{user}'@'%%' = PASSWORD('{pass}');
                """.format(**{
            'db': connection.escape_string(database),
            'olddb': connection.escape_string(old_database),
            'user': connection.escape_string(username),
            'pass': connection.escape_string(password)
        }), ())
    connection.commit()
    print('Update complete.')
    return {
        'Username': username,
        'EncryptedPassword': encrypt(password, database)
    }


def delete(database, username):
    """
    Delete the existing schema, revoke database-level privileges, and drop user.
    :param database: string
    :return:
    """
    with connection.cursor() as cursor:
        print('Dropping schema and user...')
        cursor.execute("""
                DELETE FROM mysql.db WHERE Db = '{db}' AND User = '{user}';
                DELETE FROM mysql.user WHERE user='{user}';
                DROP DATABASE {db};
            """.format(**{
            'db': connection.escape_string(database),
            'user': connection.escape_string(username),
        }), ())
    connection.commit()


def encrypt(value, database):
    """
    Encrypts a value using AWS KMS
    :param value: string
    :return: string
    """
    r = kmsClient.encrypt(KeyId=kmsKeyARN, Plaintext=value,
                          EncryptionContext={"Application": application, "Database": database})
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
    print('Decrypting value..')
    r = kmsClient.decrypt(CiphertextBlob=base64.b64decode(value))

    if 'Plaintext' in r:
        print('Decrypted.')
        return r['Plaintext']
    else:
        print('Invalid response from kms during decrypt:')
        print(r)
        exit()
