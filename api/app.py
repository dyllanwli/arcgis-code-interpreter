from dotenv import load_dotenv
load_dotenv()

# from api.services import create_service
from fastapi import FastAPI, UploadFile, File
from api.middlewares import upload, add_cors
from api.agents.tutor import ArcGISTutor
from api.schemas import *


from langchain.schema import messages_from_dict, messages_to_dict


app: FastAPI = FastAPI()

add_cors(app)

@app.get("/get/check")
async def health_check():
    return {"message": "Hello World"}

@app.post("/post/check")
async def test():
    return {"message": "Hello World"}

@app.post("/api/ask")
def ask(request: LangRequest) -> LangResponse:
    run_params = request.dict()
    memory = run_params.pop("memory", [])
    session_id = run_params.pop("session_id", "my-session")
    tutor = ArcGISTutor(session_id=session_id)
    agent = tutor.agent()
    output = agent.run(run_params) 
    # add error handling
    memory = (
        []
        if not agent.memory
        else messages_to_dict(agent.memory.chat_memory.messages)
    )
    return LangResponse(output=output, error="", memory=memory)

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    return await upload(file)