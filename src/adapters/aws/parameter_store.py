from typing import Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from adapters.log.logger import Logger


class AWSParameterStore:
    def __init__(self, region_name: str = "sa-east-1") -> None:
        self._logger = Logger.get_logger()
        self._client = boto3.client("ssm", region_name=region_name)

    def get_parameter(self, name: str) -> Optional[str]:
        try:
            response = self._client.get_parameter(Name=name, WithDecryption=True)
            return response["Parameter"]["Value"]
        except (BotoCoreError, ClientError) as e:
            self._logger.exception(f"Error retrieving parameter {name}: {e}")
            raise
