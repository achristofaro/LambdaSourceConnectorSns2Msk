import boto3


class GlueSchemaRegistryClient:
    def __init__(self):
        self.client = boto3.client("glue")
