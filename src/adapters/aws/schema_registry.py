import boto3


class GlueSchemaRegistryClient:
    def __init__(self):
        self.__client = boto3.client("glue")
