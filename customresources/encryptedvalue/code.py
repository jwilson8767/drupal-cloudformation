import base64
import boto3
import cfnresponse

def handler(event, context):
    if event['RequestType'] == 'Delete' or event['RequestType'] == 'Update':
        return cfnresponse.send(event, context, cfnresponse.SUCCESS, {}, None)
    client = boto3.client('kms')
    value = client.encrypt(
        KeyId=event['ResourceProperties']['KMSKeyARN'],
        Plaintext=event['ResourceProperties']['Plaintext']
    )
    return cfnresponse.send(event, context, cfnresponse.SUCCESS, {'encryptedValue': base64.b64encode(value['CiphertextBlob'])},
                            {})
