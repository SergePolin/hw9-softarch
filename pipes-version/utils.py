import os
from typing import List
from multiprocessing import Queue
from dataclasses import dataclass

STOP_WORDS: List[str] = ['bird-watching', 'ailurophobia', 'mango']

EMAIL_SENDER = os.getenv('EMAIL_SENDER', '')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
EMAIL_RECIPIENTS = os.getenv('EMAIL_RECIPIENTS', '').split(',')

class Message:
    def __init__(self, text: str, user_alias: str):
        self.text = text
        self.user_alias = user_alias

api_to_filter_queue: Queue = None
filter_to_screaming_queue: Queue = None
screaming_to_publish_queue: Queue = None

BAD_WORDS: List[str] = ['bird-watching', 'ailurophobia', 'mango']

@dataclass
class PipelineStats:
    messages_processed: int = 0
    total_processing_time: float = 0.0
    max_latency: float = 0.0
    min_latency: float = float('inf')
    
    @property
    def avg_processing_time(self) -> float:
        return self.total_processing_time / self.messages_processed if self.messages_processed > 0 else 0