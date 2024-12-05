import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import aio_pika
import sys
import os
from contextlib import asynccontextmanager

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import get_rabbitmq_url, FILTER_QUEUE

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.rabbitmq = await get_rabbitmq_connection()
    app.state.channel = await app.state.rabbitmq.channel()
    await app.state.channel.declare_queue(FILTER_QUEUE, durable=True)
    
    yield
    
    await app.state.rabbitmq.close()

app = FastAPI(title="Message API Service", lifespan=lifespan)

class Message(BaseModel):
    text: str
    user_alias: str

async def get_rabbitmq_connection():
    return await aio_pika.connect_robust(get_rabbitmq_url())

@app.post("/message")
async def send_message(message: Message):
    try:
        rabbitmq_message = aio_pika.Message(
            body=f"{message.text}|{message.user_alias}".encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        )
        
        await app.state.channel.default_exchange.publish(
            rabbitmq_message,
            routing_key=FILTER_QUEUE
        )
        
        return {"status": "Message sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    try:
        if not app.state.rabbitmq or app.state.rabbitmq.is_closed:
            raise HTTPException(status_code=503, detail="RabbitMQ connection is not available")
        return {"status": "healthy"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)