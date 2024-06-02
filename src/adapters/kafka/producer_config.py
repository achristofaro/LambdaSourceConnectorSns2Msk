import socket
from adapters.aws.oauth import IamOAuth
from helpers.config import ConfigLoader


class KafkaConfig():

    def __init__(self,):
        self._config = ConfigLoader.get_config()
        self._kafka_config = self._config['KAFKA']
        self._aws_config = self._config['AWS']

    def get_kafka_config(self,) -> dict[str, str]:
        return self._kafka_config

    def get_kafka_producer_config(self,) -> dict:

        return {
            'bootstrap.servers': self._kafka_config['bootstrap_servers'],
            'client.id': f"{self._kafka_config['client_id']}: {socket.gethostname()}",
            'socket.timeout.ms': 1000,
            'socket.keepalive.enable': True,
            'api.version.request': True,
            'security.protocol': 'SASL_SSL',
            'sasl.mechanisms': 'OAUTHBEARER',
            'oauth_cb': lambda x: IamOAuth.get_token(region=self._aws_config['region'], role_arn=self._aws_config['role_arn']),
            'batch.num.messages': 100,
            'linger.ms': 5,
            'batch.size': 32 * 1024,
            'compression.type': 'gzip',
            'message.max.bytes': 8 * 1024,
            'max.request.size': 1024 * 1024,
            'buffer.memory': 110 * 1024 * 1024,
            'acks': 'all',
            'enable.idempotence': True,
            'max.in.flight.requests.per.connection': 5,
            'retries': 3,
            'retry.backoff.ms': 300,
            'delivery.timeout.ms': 5 * 60 * 1000
        }
