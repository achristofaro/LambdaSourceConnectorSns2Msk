from adapters.log.logger import Logger
from adapters.kafka.producer import KafkaProducer
from domain.use_case.publish_message import PublishMessage
from helpers.response_handler import ResponseHandler


def lambda_handler(event, context):
    logger = Logger.configure_logging()
    response = ResponseHandler.send_response

    logger.info(f'Event received: {event}')
    try:
        producer = KafkaProducer()
        publisher = PublishMessage(producer)

        # Processa cada registro de evento recebido
        for record in event['records']:
            logger.info('Publishing message to Kafka topic: ', record)
            publisher.publish(record)

        # Deixe uma margem de tempo para evitar o término abrupto da função
        time_limit = context.get_remaining_time_in_millis()
        safe_margin = 500  # 500 ms de margem de segurança

        if time_limit > safe_margin:
            # Aguardar a entrega de todas as mensagens, mas não ultrapasse o tempo limite
            producer.flush(timeout=(time_limit - safe_margin) / 1000.0)
        else:
            logger.exception('Time limit reached, not flushing messages.')
            return response(False, 400, 'Time limit reached, not flushing messages.')

    except Exception as ex:
        logger.exception(f'Unhandled exception: {ex}')
        return response(False, 500, 'Internal Error', str(ex))

    return response(True, 200, 'All messages published to MSK successfully.')


if __name__ == '__main__':

    body = '''
        {"Records": [{"EventSource": "aws:sns"}]}
    '''
    print(lambda_handler(body, None))
