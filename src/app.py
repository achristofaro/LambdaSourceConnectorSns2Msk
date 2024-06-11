from typing import Any

from adapters.kafka.producer import KafkaProducer
from adapters.log.logger import Logger
from domain.use_case.publish_message import PublishMessage
from helpers.response_handler import ResponseHandler


def lambda_handler(event, context) -> dict[str, Any]:
    logger = Logger.get_logger()
    response = ResponseHandler.custom_response

    records = event.get("Records", [])
    num_records = len(records)
    safe_margin = 500  # milliseconds

    logger.info(
        f"Event received: {event} number of records at the event: {num_records}"
    )

    try:
        producer = KafkaProducer()
        publisher = PublishMessage(producer)

        for record in event.get("Records", []):
            logger.info(f"Submitting for publish: {record}")
            publisher.publish(record)

        # Get the remaining time in milliseconds.
        time_limit = context.get_remaining_time_in_millis()

        # Check if the time limit has been reached.
        if time_limit > safe_margin:
            logger.info(f"Flushing {producer.len()} messages...")

            # Flush the producer with a timeout of the remaining time.
            producer.flush(timeout=(time_limit - safe_margin) / 1000.0)
        else:
            logger.warning("Time limit reached, not flushing messages.")
            return response(False, 400, "Time limit reached, not flushing messages.")

    except Exception as e:
        logger.exception(f"Unhandled exception: {repr(e)}")
        return response(False, 500, "Internal Error", repr(e))

    return response(True, 200, f"{num_records} message(s) published.")
