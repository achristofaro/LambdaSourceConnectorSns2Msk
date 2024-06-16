from typing import Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from adapters.log.logger import Logger


class AWSParameterStore:
    def __init__(self, region_name: str = "sa-east-1") -> None:
        self.__logger = Logger.get_logger()
        self.__client = boto3.client("ssm", region_name=region_name)

    def get_parameter(self, name: str) -> Optional[str]:
        try:
            response = self.__client.get_parameter(Name=name, WithDecryption=True)
            return response["Parameter"]["Value"]
        except (BotoCoreError, ClientError) as e:
            self.__logger.exception(f"Error retrieving parameter {name}: {e}")
            raise
