from langchain.chains import LLMMathChain
from langchain.agents.tools import Tool
from langchain.chains.router import MultiRetrievalQAChain

from langchain.llms import BaseLLM
from .retrievers import get_retrievers

def documentation_tool(llm: BaseLLM):
    retriever_infos = get_retrievers()
    chain = MultiRetrievalQAChain.from_retrievers(llm, retriever_infos)
    return Tool(
        name = "ArcGIS Documentation Helper",
        func = chain.run,
        description="useful for when you need to answer questions about ArcGIS"
    )


def math_tool(llm: BaseLLM):
    chain = LLMMathChain.from_llm(llm=llm, verbose=True)
    return Tool(
        name="Calculator",
        func=chain.run,
        description="useful for when you need to answer questions about math"
    )