from adapters.log.logger import Logger
from adapters.kafka.producer import KafkaProducer
from domain.use_case.publish_message import PublishMessage
from helpers.response_handler import ResponseHandler


def lambda_handler(event, context):
    logger = Logger.get_logger()
    response = ResponseHandler.custom_response

    records = event.get('Records', [])
    num_records = len(records)

    logger.info(f'Event received: {event}')
    logger.info(f'Number of records received: {num_records}')

    try:
        producer = KafkaProducer()
        publisher = PublishMessage(producer)

        for record in event.get('Records', []):
            logger.info(f'Submitting for publish: {record}')
            publisher.publish(record)

        # Deixe uma margem de tempo para evitar o término abrupto da função
        time_limit = context.get_remaining_time_in_millis()
        safe_margin = 500  # 500 ms de margem de segurança

        if time_limit > safe_margin:
            # Aguardar a entrega de todas as mensagens, mas não ultrapasse o tempo limite
            logger.info(f'Flushing {producer.len()} messages...')
            producer.flush(timeout=(time_limit - safe_margin) / 1000.0)
        else:
            logger.warning('Time limit reached, not flushing messages.')
            return response(False, 400, 'Time limit reached, not flushing messages.')

    except Exception as e:
        logger.exception(f'Unhandled exception: {repr(e)}')
        return response(False, 500, 'Internal Error', repr(e))

    return response(True, 200, f'{num_records} message(s) received and {producer.len()} ')
