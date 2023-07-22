from langchain.chains import LLMMathChain
from langchain.agents.tools import Tool
from langchain.chains.router import MultiRetrievalQAChain

from langchain.llms import BaseLLM
from .retrievers import get_retrievers, get_code_retrievers

from langchain.chains import ConversationChain
from langchain.llms import OpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)

llm = OpenAI(temperature=0)

def documentation_tool(llm: BaseLLM):
    retriever_infos = get_retrievers()
    chain = MultiRetrievalQAChain.from_retrievers(llm, retriever_infos)
    return Tool(
        name = "ArcGIS Documentation Helper",
        func = chain.run,
        description="useful for when you need to answer questions about ArcGIS"
    )

def arcgis_code_sample(llm: BaseLLM):
    retriever_infos = get_code_retrievers()
    chain = MultiRetrievalQAChain.from_retrievers(llm, retriever_infos)
    return Tool(
        name = "ArcGIS Code Sample Helper",
        func = chain.run,
        description="useful for when you need to generate ArcGIS code samples or ask questions about ArcGIS code samples"
    )

def math_tool(llm: BaseLLM):
    chain = LLMMathChain.from_llm(llm=llm, verbose=True)
    return Tool(
        name="Calculator",
        func=chain.run,
        description="useful for when you need to answer questions about math"
    )
    
def general_assitant(llm: BaseLLM, memory=None):

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                "The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know."  # noqa
            ),
            MessagesPlaceholder(variable_name="memory"),
            HumanMessagePromptTemplate.from_template("{input}"),
        ]
    )
    chain = ConversationChain(memory=memory, prompt=prompt, llm=llm)
    return Tool(
        name="General Assitant",
        func=chain.run,
        description="useful for when you need to answer questions that not related to other tools"
    )