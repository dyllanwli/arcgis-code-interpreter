from typing import Any
from pydantic import BaseModel

class LangRequest(BaseModel):
    input: str
    memory: list[dict[str, Any]]
    session_id: str


class MemoryData(BaseModel):
    content: str
    additional_kwargs: dict[str, Any]


class Memory(BaseModel):
    type: str
    data: MemoryData


class LangResponse(BaseModel):
    output: str
    error: str
    memory: list[Memory]


class LangResponseDocuments(LangResponse):
    source_documents: list[str]
