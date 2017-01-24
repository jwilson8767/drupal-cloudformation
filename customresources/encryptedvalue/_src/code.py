from __future__ import print_function
import base64
import boto3
import cfnresponse


def handler(event, context):
    print(event)
    if event['RequestType'] == 'Delete' or event['RequestType'] == 'Update':
        return cfnresponse.send(event, context, cfnresponse.SUCCESS)
    client = boto3.client('kms')
    value = client.encrypt(
        KeyId=event['ResourceProperties']['KMSKeyARN'],
        Plaintext=event['ResourceProperties']['Plaintext']
    )
    if "CiphertextBlob" in value:
        return cfnresponse.send(event, context, cfnresponse.SUCCESS,
                                response_data={'encryptedValue': base64.b64encode(value['CiphertextBlob'])})
    else:
        print("Response:")
        print(value)
        return cfnresponse.send(event, context, cfnresponse.FAILED)
