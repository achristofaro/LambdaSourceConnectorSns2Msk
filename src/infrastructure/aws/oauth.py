from aws_msk_iam_sasl_signer import MSKAuthTokenProvider
from infrastructure.log.logger import Logger


class IamOAuth:

    @staticmethod
    def get_token(**kwargs) -> tuple[str, float]:
        _logger = Logger.configure_logging()

        try:
            if "arn_role" in kwargs:
                auth_token, expiry_ms = (MSKAuthTokenProvider.generate_auth_token_from_role_arn(kwargs["region"], kwargs["arn_role"]))
            else:
                auth_token, expiry_ms = MSKAuthTokenProvider.generate_auth_token(kwargs["region"])

            return auth_token, expiry_ms / 1000

        except Exception as ex:
            _logger.exception(f'Unexpected error during auth token generation: {ex}')
            raise Exception(ex)
