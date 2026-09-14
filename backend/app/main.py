import logging
import uuid

import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

from agent import get_response
from config import env
from db import init_db
from logger import setup_logging
from schema.chat_request import ChatRequest

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Starting application — initialising database")
    init_db()
    logging.info("Database initialised with seed data")
    yield
    logging.info("Shutting down application")


app = FastAPI(title="Nova Loan Agent", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health():
    return {"status": "ok", "agent": "Nova"}


@app.post("/chat")
async def chat(chat: ChatRequest, response: Response):
    try:
        thread_id = chat.thread_id or uuid.uuid4().hex

        agent_response = await get_response(chat.prompt, session_id=thread_id)

        return {
            "response": agent_response,
            "thread_id": thread_id,
        }
    except Exception as e:
        logging.error(f"Chat error: {e}", exc_info=True)
        response.status_code = 500
        return {"error": "An error occurred"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=env.ENVIRONMENT == "dev",
        log_level="info",
    )
