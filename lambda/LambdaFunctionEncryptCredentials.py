import base64
import boto3
import cfnresponse
def handler(event, context):
    if event['RequestType'] == 'Delete':
        return cfnresponse.send(event,context,cfnresponse.SUCCESS,{})
    client = boto3.client('kms')
    encryptedUsername = client.encrypt(
        KeyId=event['ResourceProperties']['KMSKeyARN'],
        Plaintext=event['ResourceProperties']['Username']
    )
    encryptedPassword = client.encrypt(
        KeyId=event['ResourceProperties']['KMSKeyARN'],
        Plaintext=event['ResourceProperties']['Password']
    )
    return cfnresponse.send(event,context,cfnresponse.SUCCESS,{
        'encryptedUsername': base64.b64encode(encryptedUsername['CiphertextBlob']),
        'encryptedPassword': base64.b64encode(encryptedPassword['CiphertextBlob'])
    },{})
