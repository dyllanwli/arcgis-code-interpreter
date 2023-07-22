from starlette.responses import JSONResponse
import threading
from utils import delete_file
from fastapi import UploadFile, File

async def upload(file: UploadFile = File(...)):
    with open(f"{file.filename}", "wb") as buffer:
        buffer.write(await file.read())
    threading.Timer(1800, delete_file, args=[file.filename]).start()
    return JSONResponse(status_code=200, content={"message": "File uploaded successfully"})
    