import os

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from router.router import route

ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get("ALLOWED_ORIGINS", "*").split(",")
    if origin.strip()
]

app = FastAPI(title="LLM Router API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["POST"],
    allow_headers=["*"],
)


class RouteRequest(BaseModel):
    prompt: str
    recent_context: str = ""


@app.post("/route")
def route_prompt(body: RouteRequest):
    if not body.prompt.strip():
        return {"tier": None, "reason": "empty_prompt", "source": "none", "confidence": 0.0}
    return route(body.prompt, recent_context=body.recent_context)


@app.get("/health")
def health():
    return {"status": "ok"}
