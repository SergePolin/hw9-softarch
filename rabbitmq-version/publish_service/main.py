import asyncio
import aio_pika
import yagmail
import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import (
    get_rabbitmq_url, PUBLISH_QUEUE,
    EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECIPIENTS
)

email_client = None
if all([EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECIPIENTS]):
    try:
        email_client = yagmail.SMTP(EMAIL_SENDER, EMAIL_PASSWORD)
        print("Email client initialized successfully")
    except Exception as e:
        print(f"Failed to initialize email client: {str(e)}")

async def simulate_email_send(subject: str, body: str, recipients: list):
    await asyncio.sleep(0.1 + (time.time() % 0.1))
    print(f"[SIMULATED] Email sent:")
    print(f"To: {', '.join(recipients)}")
    print(f"Subject: {subject}")
    print(f"Body: {body}\n")

async def send_email(subject: str, body: str, recipients: list):
    if email_client is not None:
        try:
            email_client.send(
                to=recipients,
                subject=subject,
                contents=body
            )
            print(f"Real email sent to {', '.join(recipients)}")
            return True
        except Exception as e:
            print(f"Failed to send real email: {str(e)}")
            await simulate_email_send(subject, body, recipients)
            return False
    else:
        await simulate_email_send(subject, body, recipients)
        return False

async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        text, user_alias = message.body.decode().split('|')
        
        subject = f"New Message from {user_alias}"
        body = f"Message: {text}"
        
        success = await send_email(subject, body, EMAIL_RECIPIENTS)
        status = "sent" if success else "simulated"
        print(f"Email {status} for message from {user_alias}")

async def main():
    connection = await aio_pika.connect_robust(get_rabbitmq_url())
    
    async with connection:
        channel = await connection.channel()
        
        publish_queue = await channel.declare_queue(PUBLISH_QUEUE, durable=True)
        
        print(" [*] Publish Service waiting for messages. To exit press CTRL+C")
        print(" [*] Email mode:", "REAL" if email_client else "SIMULATION")
        await publish_queue.consume(process_message)
        
        try:
            await asyncio.Future()
        except asyncio.CancelledError:
            pass

if __name__ == "__main__":
    asyncio.run(main())