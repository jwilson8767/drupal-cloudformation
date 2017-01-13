import base64
import boto3
import cfnresponse


def handler(event, context):
    if event['RequestType'] == 'Delete':
        return cfnresponse.send(event, context, cfnresponse.SUCCESS, {}, None)
    client = boto3.client('kms')
    encrypted_username = client.encrypt(
        KeyId=event['ResourceProperties']['KMSKeyARN'],
        Plaintext=event['ResourceProperties']['Username']
    )
    encrypted_password = client.encrypt(
        KeyId=event['ResourceProperties']['KMSKeyARN'],
        Plaintext=event['ResourceProperties']['Password']
    )
    return cfnresponse.send(event, context, cfnresponse.SUCCESS, {
        'encryptedUsername': base64.b64encode(encrypted_username['CiphertextBlob']),
        'encryptedPassword': base64.b64encode(encrypted_password['CiphertextBlob'])
    }, {})
