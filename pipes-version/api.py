from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager
import uvicorn

from main import Pipeline

class Message(BaseModel):
    text: str
    user_alias: str

class HealthResponse(BaseModel):
    status: str = "healthy"

class MessageResponse(BaseModel):
    status: str
    processed_text: str | None = None
    error: str | None = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pipeline = Pipeline()
    app.state.pipeline.start()
    print("Pipeline started")
    
    yield
    
    app.state.pipeline.shutdown()
    print("Pipeline shut down")

app = FastAPI(lifespan=lifespan)

@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse()

@app.post("/message", response_model=MessageResponse)
async def process_message(message: Message):
    try:
        result = app.state.pipeline.process_message(message.text)
        
        if not result:
            return MessageResponse(
                status="filtered",
                processed_text=None,
                error="Message contained stop words"
            )
        
        return MessageResponse(
            status="success",
            processed_text=result
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

def run_server():
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )

if __name__ == "__main__":
    run_server()