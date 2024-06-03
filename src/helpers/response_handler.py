from typing import Union


class ResponseHandler:

    @classmethod
    def custom_response(cls, success: bool, status_code: int,
                      message: str, ex: Union[str, None] = None) -> dict[str, Union[bool, int, str]]:
        response = {
            'success': success,
            'statusCode': status_code,
            'Message': message,
            'ExceptionMessage': ex
        }

        filtered_response = {k: v for k, v in response.items() if v is not None}

        return filtered_response