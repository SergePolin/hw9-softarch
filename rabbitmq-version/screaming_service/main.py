import asyncio
import aio_pika
import aiormq
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import get_rabbitmq_url, SCREAMING_QUEUE, PUBLISH_QUEUE

async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        text, user_alias = message.body.decode().split('|')
        
        screamed_text = text.upper()
        
        await message.channel.basic_publish(
            f"{screamed_text}|{user_alias}".encode(),
            routing_key=PUBLISH_QUEUE,
            exchange="",
            properties=aiormq.spec.Basic.Properties(
                delivery_mode=2
            )
        )
        print(f"Converted message from {user_alias} to uppercase")

async def main():
    connection = await aio_pika.connect_robust(
        get_rabbitmq_url(),
        reconnect_interval=5
    )
    
    async with connection:
        channel = await connection.channel()
        
        screaming_queue = await channel.declare_queue(
            SCREAMING_QUEUE, 
            durable=True,
            auto_delete=False
        )
        await channel.declare_queue(
            PUBLISH_QUEUE, 
            durable=True,
            auto_delete=False
        )
        
        print(" [*] SCREAMING Service waiting for messages. To exit press CTRL+C")
        await screaming_queue.consume(process_message)
        
        try:
            await asyncio.Future()
        except asyncio.CancelledError:
            pass

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutting down...")