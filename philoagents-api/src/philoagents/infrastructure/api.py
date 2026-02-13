from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from philoagents.domain.philosopher_factory import PhilosopherFactory
from philoagents.application.conversation_service.generate_response import get_response

from philoagents.application.conversation_service.reset_conversation import reset_conversation_state
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    message: str
    philosopher_id: str
    
@app.post("/chat")
async def chat(chat_message: ChatMessage):
    try:
        philosopher_factory = PhilosopherFactory()
        philosopher = philosopher_factory.get_philosopher(chat_message.philosopher_id)

        response, _  = await get_response(
            messages=chat_message.message,
            philosopher_id = chat_message.philosopher_id,
            philosopher_name = philosopher.name,
            philosopher_style = philosopher.style,
            philosopher_perspective = philosopher.perspective,
            philosopher_context = ""
            )

        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/reset_memory")
async def reset_conversation():
    try:
        result = await reset_conversation_state()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


