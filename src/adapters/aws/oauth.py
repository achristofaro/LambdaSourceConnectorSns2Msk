from aws_msk_iam_sasl_signer import MSKAuthTokenProvider

from adapters.log.logger import Logger


class IamOAuth:

    @staticmethod
    def get_token(**kwargs) -> tuple[str, float]:
        __logger = Logger.get_logger()

        try:
            if "arn_role" in kwargs:
                auth_token, expiry_ms = (
                    MSKAuthTokenProvider.generate_auth_token_from_role_arn(
                        kwargs["region"], kwargs["role_arn"]
                    )
                )
            else:
                auth_token, expiry_ms = MSKAuthTokenProvider.generate_auth_token(
                    kwargs["region"], aws_debug_creds=True
                )

            return auth_token, expiry_ms / 1000

        except Exception as ex:
            __logger.exception(f"Unexpected error during auth token generation: {ex}")
            raise
