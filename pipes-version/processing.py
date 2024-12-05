from filter import Filter
import yagmail
import asyncio
import time

class ScreamingFilter(Filter):
    def _process(self, content: str) -> str:
        return content.upper()

class ProfanityFilter(Filter):
    def __init__(self, outputs: list, bad_words: list[str]):
        super().__init__(outputs)
        self.bad_words = bad_words

    def _process(self, content: str) -> str:
        for word in self.bad_words:
            if word.lower() in content.lower():
                return ""
        return content

class EmailFilter(Filter):
    def __init__(self, outputs: list, email_config: dict):
        super().__init__(outputs)
        self.email_sender = email_config.get('sender', '')
        self.email_password = email_config.get('password', '')
        self.email_recipients = email_config.get('recipients', [])
        
        self.email_client = None
        if all([self.email_sender, self.email_password, self.email_recipients]):
            try:
                self.email_client = yagmail.SMTP(self.email_sender, self.email_password)
                print("Email client initialized successfully")
            except Exception as e:
                print(f"Failed to initialize email client: {str(e)}")

    def _simulate_email_send(self, content: str):
        time.sleep(0.1 + (time.time() % 0.1))
        print(f"[SIMULATED] Email sent:")
        print(f"To: {', '.join(self.email_recipients)}")
        print(f"Subject: New Message")
        print(f"Body: {content}\n")

    def _process(self, content: str) -> str:
        if not content:
            return content
            
        if self.email_client is not None:
            try:
                self.email_client.send(
                    to=self.email_recipients,
                    subject="New Message",
                    contents=content
                )
                print(f"Real email sent to {', '.join(self.email_recipients)}")
            except Exception as e:
                print(f"Failed to send real email: {str(e)}")
                self._simulate_email_send(content)
        else:
            self._simulate_email_send(content)
        
        return content