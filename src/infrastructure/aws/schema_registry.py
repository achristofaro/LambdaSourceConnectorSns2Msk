import boto3
import logging


class GlueSchemaRegistryClient:
    def __init__(self):
        self.client = boto3.client('glue')