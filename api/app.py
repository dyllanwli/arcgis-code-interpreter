import os
from dotenv import load_dotenv
load_dotenv()
print("Running on API_BASE:", os.getenv("OPENAI_API_BASE"))

from api.services import create_service
from fastapi import FastAPI
from api.middlewares import upload
from fastapi import UploadFile, File

app: FastAPI = create_service(
    "api.agents.tutor:agent",
    # "api.agents.example:conversation",
    # auth_token="funkyfamily"
)

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    return await upload(file)