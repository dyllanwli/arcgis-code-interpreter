import os
from dotenv import load_dotenv
load_dotenv()
print("Running on API_BASE:", os.getenv("OPENAI_API_BASE"))

from api.services import create_service
from fastapi import FastAPI
from api.middlewares import upload

app: FastAPI = create_service(
    "api.agents.tutor:agent",
    auth_token="funkyfamily"
)

@app.post("/api/upload")
def upload_file(file):
    return upload(file)