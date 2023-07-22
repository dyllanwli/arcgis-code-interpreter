from langchain import LLMMathChain
from langchain.chains import load_chain
from langchain.agents.tools import Tool
from langchain.chat_models import ChatOpenAI
from langchain.experimental.plan_and_execute import (
    PlanAndExecute,
    load_agent_executor,
    load_chat_planner,
)
from langchain.llms import OpenAI

import logging
import pickle
from pathlib import Path
from typing import Optional
from langchain.vectorstores import VectorStore

class ArcGISTutor:
    def __init__(self):
        self.vectorstore: VectorStore = None
        self.__start__()
    
    def __start__(self, vectorstore_path: Optional[str] = "api/storage/vectorstore.pkl"):
        logging.info("loading vectorstore")
        if not Path(vectorstore_path).exists():
            raise ValueError("vectorstore.pkl does not exist, please run ingest.py first")
        with open(vectorstore_path, "rb") as f:
            self.vectorstore = pickle.load(f)
    
    def agent(self):
        llm = OpenAI(temperature=0)
        
        llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)
        llm_vectorstore_chain = load_chain("lc://chains/vector-db-qa/stuff/chain.json", vectorstore=self.vectorstore)

        tools = [
            Tool(
                name="ArcGIS Documentation Helper",
                func=llm_vectorstore_chain.run,
                description = "useful for when you need to answer questions about ArcGIS",
            ),
            Tool(
                name="Calculator",
                func=llm_math_chain.run,
                description="useful for when you need to answer questions about math",
            ),
        ]

        model = ChatOpenAI(temperature=0)
        
        planner = load_chat_planner(model)
        executor = load_agent_executor(model, tools, verbose=True)
        agent = PlanAndExecute(planner=planner, executor=executor, verbose=True)
        return agent


tutor = ArcGISTutor()
agent = tutor.agent()

if __name__ == "__main__":
    agent.run(
        "What is ArcGIS?",
    )