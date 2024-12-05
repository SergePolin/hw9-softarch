import asyncio
import aio_pika
import aiormq
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import get_rabbitmq_url, FILTER_QUEUE, SCREAMING_QUEUE, STOP_WORDS

async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        text, user_alias = message.body.decode().split('|')
        
        if any(word.lower() in text.lower() for word in STOP_WORDS):
            print(f"Message from {user_alias} filtered out due to stop words")
            return
        
        await message.channel.basic_publish(
            message.body,
            routing_key=SCREAMING_QUEUE,
            exchange="",
            properties=aiormq.spec.Basic.Properties(
                delivery_mode=2
            )
        )
        print(f"Message from {user_alias} passed filter")

async def main():
    connection = await aio_pika.connect_robust(
        get_rabbitmq_url(),
        reconnect_interval=5
    )
    
    async with connection:
        channel = await connection.channel()
        
        filter_queue = await channel.declare_queue(
            FILTER_QUEUE, 
            durable=True,
            auto_delete=False
        )
        await channel.declare_queue(
            SCREAMING_QUEUE, 
            durable=True,
            auto_delete=False
        )
        
        print(" [*] Filter Service waiting for messages. To exit press CTRL+C")
        await filter_queue.consume(process_message)
        
        try:
            await asyncio.Future()
        except asyncio.CancelledError:
            pass

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutting down...")