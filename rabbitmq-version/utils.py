import os
from typing import List

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT', 5672))
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'guest')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASS', 'guest')

FILTER_QUEUE = 'filter_queue'
SCREAMING_QUEUE = 'screaming_queue'
PUBLISH_QUEUE = 'publish_queue'

STOP_WORDS: List[str] = ['bird-watching', 'ailurophobia', 'mango']

EMAIL_SENDER = os.getenv('EMAIL_SENDER', '')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
EMAIL_RECIPIENTS = os.getenv('EMAIL_RECIPIENTS', '').split(',')

def get_rabbitmq_url() -> str:
    return f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/'