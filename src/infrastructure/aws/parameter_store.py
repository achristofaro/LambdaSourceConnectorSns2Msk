import boto3


class AWSParameterStore:
    def __init__(self, region_name='sa-east-1'):
        self._client = boto3.client('ssm', region_name=region_name)

    def get_parameter(self, name: str):
        response = self._client.get_parameter(Name=name, WithDecryption=True)
        return response['Parameter']['Value']