from locust import HttpUser, task, between
import random

class MessageUser(HttpUser):
    wait_time = between(1, 2)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_messages = [
            "Hello, this is a test message!",
            "Testing the system performance",
            "Another test message for load testing",
            "bird-watching is fun",
            "I love mangos",
            "Someone with ailurophobia",
            "This message should pass through",
            "Load testing in progress",
            "Final test message"
        ]
    
    @task
    def send_message(self):
        message = random.choice(self.test_messages)
        payload = {
            "text": message,
            "user_alias": f"tester_{self.user_id}"
        }
        self.client.post("/message", json=payload)