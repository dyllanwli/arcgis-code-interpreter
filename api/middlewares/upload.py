from starlette.responses import JSONResponse
from fastapi import UploadFile, File

async def upload(file: UploadFile = File(...)):
    data = await file.read()
    if not file.filename.endswith(".zip"):
        return JSONResponse(status_code=400, content={"message": "File must be a zip shapefile"})
    with open("cache/shapefile.zip", "wb") as buffer:
        buffer.write(data)
    return JSONResponse(status_code=200, content={"message": "File uploaded successfully"})
    