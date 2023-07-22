from langcorn import create_service
from fastapi import FastAPI
from fastapi import UploadFile, File

from middlewares import upload

app: FastAPI = create_service(
    "api.agents.tutor:agent",
    auth_token="funkyfamily"
)

@app.post("/api/upload")
def upload_file(file: UploadFile = File(...)):
    return upload(file)