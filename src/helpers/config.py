import os
import logging
from typing import Optional
from adapters.aws.parameter_store import AWSParameterStore


class ConfigLoader:
    _config : Optional[dict] = {}

    def __init__(self,):
        self._parameter_store = AWSParameterStore()

    def __load(self,):

        self._config = {
            'KAFKA': {
                'bootstrap_servers': os.getenv(
                    'KAFKA_BROKER',
                    (
                        'b-2.mskesblab.fkyhwv.c4.kafka.sa-east-1.amazonaws.com:9098,'
                        'b-1.mskesblab.fkyhwv.c4.kafka.sa-east-1.amazonaws.com:9098,'
                        'b-3.mskesblab.fkyhwv.c4.kafka.sa-east-1.amazonaws.com:9098'
                    )
                ) or self._parameter_store.get_parameter('/lambdaSourceConnectorSns2Msk/kafka/broker'),
                'topic': os.getenv(
                    'KAFKA_TOPIC',
                    'aws-msk-blc-caphub-assestscdb-V1-dev-n'
                ) or self._parameter_store.get_parameter('/lambdaSourceConnectorSns2Msk/kafka/topic'),
                'topic_dlq': os.getenv(
                    'KAFKA_TOPIC',
                    'aws-msk-blc-caphub-assestscdb-V1-dl-dev-n'
                ) or self._parameter_store.get_parameter('/lambdaSourceConnectorSns2Msk/kafka/topic_dlq'),
                'client_id': os.getenv(
                    'KAFKA_CLIENT_ID',
                    'LambdaSourceConnectorSns2Msk'
                ) or self._parameter_store.get_parameter('/lambdaSourceConnectorSns2Msk/kafka/client_id')
            },
            'AWS': {
                'region': os.getenv('AWS_REGION', 'sa-east-1') or self._parameter_store.get_parameter('/lambdaSourceConnectorSns2Msk/kafka/aws_region'),
                'role_arn': os.getenv('AWS_ROLE_ARN', None) or self._parameter_store.get_parameter('/lambdaSourceConnectorSns2Msk/kafka/kafka_acks')
            },
            'LOGGING': {
                'level': os.getenv('LOGGING_LEVEL', logging.INFO) or self._parameter_store.get_parameter('/lambdaSourceConnectorSns2Msk/kafka/logging_level')
            }
        }

    @classmethod
    def get_config(cls,) -> dict:
        if cls._config is None:
            loader = cls()
            loader.__load()
        return cls._config
