from multiprocessing import Queue, Event
from datetime import datetime
import signal
import sys
import time

from filter import Message
from processing import ScreamingFilter, ProfanityFilter, LoggingFilter, EmailFilter
from utils import BAD_WORDS, PipelineStats, EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECIPIENTS

class Pipeline:
    def __init__(self):
        self.shutdown_event = Event()
        self.stats = PipelineStats()
        self.sink_pipe = Queue()
        
        self.email = EmailFilter(
            outputs=[self.sink_pipe],
            email_config={
                'sender': EMAIL_SENDER,
                'password': EMAIL_PASSWORD,
                'recipients': EMAIL_RECIPIENTS
            }
        )
        self.logging = LoggingFilter(outputs=[self.email.input])
        self.profanity = ProfanityFilter(
            outputs=[self.logging.input],
            bad_words=BAD_WORDS
        )
        self.screaming = ScreamingFilter(outputs=[self.profanity.input])
        
        self.filters = [self.screaming, self.profanity, self.logging, self.email]
        self.source_pipe = self.screaming.input

    def start(self):
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        for f in self.filters:
            f.start()

    def process_message(self, content: str) -> str:
        start_time = time.time()
        
        self.source_pipe.put(Message(
            content=content,
            created_at=datetime.now()
        ))
        
        result = self.sink_pipe.get()
        
        processing_time = time.time() - start_time
        self.stats.messages_processed += 1
        self.stats.total_processing_time += processing_time
        self.stats.max_latency = max(self.stats.max_latency, processing_time)
        self.stats.min_latency = min(self.stats.min_latency, processing_time)
        
        return result.content

    def shutdown(self):
        print("\nShutting down pipeline...")
        self.shutdown_event.set()
        
        for f in self.filters:
            f.join(timeout=5.0)
            if f.is_alive():
                f.terminate()
        
        print("\nPipeline Statistics:")
        print(f"Messages Processed: {self.stats.messages_processed}")
        print(f"Average Processing Time: {self.stats.avg_processing_time:.3f}s")
        print(f"Maximum Latency: {self.stats.max_latency:.3f}s")
        print(f"Minimum Latency: {self.stats.min_latency:.3f}s")

    def _signal_handler(self, signum, frame):
        self.shutdown()
        sys.exit(0)

def run_performance_test():
    pipeline = Pipeline()
    pipeline.start()
    
    messages = [
        "Hello World!",
        "This contains bird-watching which should be filtered",
        "THIS IS ALREADY SCREAMING",
        "Testing mango filtering",
        "A normal message that should pass through"
    ] * 20
    
    try:
        for msg in messages:
            result = pipeline.process_message(msg)
            print(f"Input: {msg}")
            print(f"Output: {result}\n")
    finally:
        pipeline.shutdown()

if __name__ == "__main__":
    run_performance_test()