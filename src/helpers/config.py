import os
from adapters.aws.parameter_store import AWSParameterStore


class ConfigLoader:
    _config = {}

    def __init__(self,):
        self._parameter_store = AWSParameterStore()

    def __load(self,):

        self._config = {
            'KAFKA': {
                'bootstrap_servers': os.getenv('KAFKA_BROKER') or self._parameter_store.get_parameter('/lambdaSourceConnectorSns2Msk/kafka/broker'),
                'topic': os.getenv('KAFKA_TOPIC') or self._parameter_store.get_parameter('/lambdaSourceConnectorSns2Msk/kafka/topic'),
                'topic_dlq': os.getenv('KAFKA_TOPIC') or self._parameter_store.get_parameter('/lambdaSourceConnectorSns2Msk/kafka/topic_dlq'),
                'client_id': os.getenv('KAFKA_CLIENT_ID') or self._parameter_store.get_parameter('/lambdaSourceConnectorSns2Msk/kafka/client_id')
            },
            'AWS': {
                'region': os.getenv('AWS_REGION') or self._parameter_store.get_parameter('/lambdaSourceConnectorSns2Msk/kafka/aws_region'),
                'role_arn': os.getenv('AWS_ROLE_ARN') or self._parameter_store.get_parameter('/lambdaSourceConnectorSns2Msk/kafka/kafka_acks')
            },
            'LOGGING': {
                'level': os.getenv('LOGGING_LEVEL') or self._parameter_store.get_parameter('/lambdaSourceConnectorSns2Msk/kafka/logging_level')
            }
        }

    @classmethod
    def get_config(cls,) -> dict:
        if cls._config is None:
            loader = cls()
            loader.__load()
        return cls._config
