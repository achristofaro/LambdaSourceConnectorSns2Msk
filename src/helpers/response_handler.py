from typing import Union


class ResponseHandler:

    @classmethod
    def send_response(cls, success: bool, status_code: int,
                      message: str, ex_message: Union[str, None] = None):
        return {'success': success,
                'statusCode': status_code,
                'ShortMessage': message,
                'DetailedMessage': ex_message}
