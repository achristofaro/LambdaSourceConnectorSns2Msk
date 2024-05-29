import logging
import os
import socket
import json
from confluent_kafka import Producer
from aws_msk_iam_sasl_signer import MSKAuthTokenProvider


bs='b-1.mskesblab.fkyhwv.c4.kafka.sa-east-1.amazonaws.com:9098,b-2.mskesblab.fkyhwv.c4.kafka.sa-east-1.amazonaws.com:9098,b-3.mskesblab.fkyhwv.c4.kafka.sa-east-1.amazonaws.com:9098'

kafka_bootstrap_servers = (lambda x: os.environ.get(x, default=bs)) ('KAFKA_BOOTSTRAP_SERVERS')
kafka_topic = (lambda x: os.environ.get(x, default='rf-cdb-ifa')) ('MSK_TOPIC_NAME')
region = (lambda x: os.environ.get(x, default='sa-east-1')) ('AWS_REGION') 
arn_role = (lambda x: os.environ.get(x, default='arn:aws:iam::324296149033:role/aws-reserved/sso.amazonaws.com/AWSReservedSSO_AWSAdministratorAccess_7223d78d1310ed2f')) ('AWS_ROLE_ARN')


def sendResponse(success, statusCode, message, responseData):
    return {
        'success' : success,
        'statusCode' : statusCode,
        'message': message,
        'responseData' : responseData
    }


def oauth_cb(oauth_config):
    auth_token=None
    expiry_ms=None
    
    try:
        # auth_token, expiry_ms = MSKAuthTokenProvider.generate_auth_token_from_role_arn(region, arn_role)
        auth_token, expiry_ms = MSKAuthTokenProvider.generate_auth_token(region)
    except Exception as ex:
        logging.exception(f'Message delivery failed: {ex}')
        os.sys.exit(1, ex)
    return auth_token, expiry_ms/1000


producer_config = { 
        'bootstrap.servers': kafka_bootstrap_servers,
        'client.id': f'lambda-producer-blc-rf: {socket.gethostname()}',
        'socket.timeout.ms': 1000,
        'socket.keepalive.enable': True,
        'api.version.request': True,

        # Autenticação
        'security.protocol': 'SASL_SSL',
        'sasl.mechanisms': 'OAUTHBEARER',
        'oauth_cb': oauth_cb,

        # Confiabilidade e idempotência
        'acks': 'all',
        'enable.idempotence': True,
        'max.in.flight.requests.per.connection': 5,

        # Retentativas e timeout
        'retries': 3,
        'retry.backoff.ms': 300,
        'delivery.timeout.ms': 5 * 60 * 1000,
        
        }


def acked(ex, msg):
    """
    Callback method
    """
    if ex is not None:
        logging.exception(f'Message delivery failed: {ex}')
    else:
        logging.info(f'Message delivered to topic: {msg.topic()} [{msg.partition()}]')


def send_message_async(producer, msg):
    """
    Publish Data
    """
    logging.info(f'Sending message: {msg} to Topic {kafka_topic}')

    try:
        msg_json_str = json.dumps({'data': msg})
        # Produzir mensagem (envio assíncrono para cada mensagem)
        producer.produce(
            kafka_topic,
            key=None,
            value=msg_json_str.encode('utf-8'),
            callback=acked
        )

        # Disparar a entrega e continuar (não bloqueia)
        producer.poll(0)

    except Exception as ex:
        logging.exception(f'Error: {ex}')


def lambda_handler(event, context):
    logging.info(f'Event Received: {event}')


    try:
        producer = Producer(**producer_config)
        
        for record in event['Records']:
            sns_message = f"{record['Sns']['Message']}: {context.aws_request_id}"
            
            logging.info(f'Publishing message to Kafka topic: {sns_message}')
            send_message_async(producer, sns_message)

        # Deixe uma margem de tempo para evitar o término abrupto da função
        time_limit = context.get_remaining_time_in_millis()
        safe_margin = 500 # 500 ms de margem de segurança

        if time_limit > safe_margin:
            # Aguardar a entrega de todas as mensagens, mas não ultrapasse o tempo limite
            producer.flush(timeout=(time_limit - safe_margin) / 1000.0)
        else:
            logging.warn('Time limit reached, not flushing messages.')
            return sendResponse(False, 400, 'Error in fetch booked appointments', [])

    except Exception as ex:
        logging.exception(f'Error: {ex}')
        return sendResponse(False, 500, 'Exception Error', str(ex))

    return sendResponse(True, 200, 'All messages published to MSK successfully.', [])