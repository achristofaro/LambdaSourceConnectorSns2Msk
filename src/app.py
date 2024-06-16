import json
from typing import Any

from adapters.kafka.producer import KafkaProducer
from adapters.log.logger import Logger
from helpers.response_handler import ResponseHandler
from use_cases.publish_message import PublishMessage

SAFE_MARGIN = 500  # milliseconds


def lambda_handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    logger = Logger.get_logger()
    response = ResponseHandler.custom_response

    records = event.get("Records", [])
    num_records = len(records)

    logger.info(
        f"Event received: {event} number of records at the event: {num_records}"
    )

    try:
        producer = KafkaProducer()
        publisher = PublishMessage(producer)

        for record in records:
            sns_message = json.loads(record.get("Sns", {}).get("Message"))
            if sns_message:
                logger.info(f"Submitting for publish: {sns_message}")
                publisher.publish(sns_message)

        # Get the remaining time in milliseconds.
        time_limit = context.get_remaining_time_in_millis()

        # Check if the time limit has been reached.
        if time_limit > SAFE_MARGIN:
            logger.info(f"Flushing {producer.len()} messages...")

            # Flush the producer with a timeout of the remaining time.
            producer.flush(timeout=(time_limit - SAFE_MARGIN) / 1000.0)
        else:
            logger.warning("Time limit reached, not flushing messages.")
            return response(False, 400, "Time limit reached, not flushing messages.")

    except Exception as e:
        logger.exception(f"Unhandled exception: {repr(e)}")
        return response(False, 500, "Internal Error", repr(e))

    return response(True, 200, f"{num_records} message(s) published.")


if __name__ == "__main__":
    event = {
        "Records": [
            {
                "EventSource": "aws:sns",
                "EventVersion": "1.0",
                "EventSubscriptionArn": "arn:aws:sns:sa-east-1:",
                "Sns": {
                    "Type": "Notification",
                    "MessageId": "b9a881c3-f4e9-5a1a-90c0-df1015e39b3d",
                    "TopicArn": "arn:aws:sns:sa-east-1",
                    "Subject": None,
                    "Message": '{"event_id": "0fe62aff-83f8-49bc-a157-2bb0ad9e6dd4", "event_type": "PDD_asset_registration_success", "org_id": "PDD-TN-c20e93c8-6f6d-4ed5-9d2b-b3990dd696a8", "schema_version": 1, "cid": "PDD001000191000000000010017081", "timestamp": "2024-05-31T14:29:30.701409", "domain": "assets", "data": {"asset": {"id": "750277123821", "asset_type": "cdb", "issuer_id": "12345678", "registration_mode": "single", "issuing_date": "2024-05-31", "maturity_date": "2025-05-31", "issued_units": 7008817.31, "unit_value": 7441.71, "index_type": "di", "index_rate": 952.47, "currency": "986", "isin_code": "", "early_redemption_terms": "no", "additional_data": {"accrual_frequency": "daily"}}, "quota": {"id": "c69a3ffa-8fb6-497b-ae30-b06dd36bfc03", "customer_name": "Cliente PJ 00000003000559", "customer_document_number": "00000003000559", "type": "legal", "purchased_units": 8306566.95, "external_id": "001000191000000000010017081"}, "created_at": "2024-05-31T14:29:30.701505"}}',
                    "Timestamp": "2024-05-31T14:29:30.981Z",
                    "SignatureVersion": "1",
                    "Signature": "XKWk50/vIJpWaZB80HR7+/bSf2r6N3Ul52fdYgQQK2BsKJH1P9Fdx8Oq03qvZOWCJa/GN4aggJ+OxqGB16O802l+K52QX/pAeJR8Y3a6Cmmm4EGk0927MdINNDvJZqSPqY0ruZt3+rYejZrk9Kgr9BdzTpzYqyJkDiDcagHP77mL9xtUa+32Y9otz5qvIO1G4m/mMeMF6yVYy0RxU23NOwa7faJ2EEM+cY3vBoL9cDR7qc/d+BBGoJpsuAG49MoY6TZelupTV32R75O9TfF4Qt3oqVyeOUIhZ7wiz2jFES1KPTvk4iapnryxMdPofCZtC6zh6Q/4nVSG5JZbW2tNHg==",
                    "SigningCertUrl": "https://sns.sa-east-1.amazonaws.com/SimpleNotificationService",
                    "UnsubscribeUrl": "https://sns.sa-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:sa-east-1",
                    "MessageAttributes": {},
                },
            }
        ]
    }

    r = lambda_handler(event, None)
    print(r)
