import os
from langchain.chat_models import AzureChatOpenAI, ChatOpenAI
# from langchain.experimental.plan_and_execute import (
#     PlanAndExecute,
#     load_agent_executor,
#     load_chat_planner,
# )
from langchain.chains import LLMChain
from langchain.llms import AzureOpenAI, OpenAI
from langchain.memory.chat_message_histories import RedisChatMessageHistory
from langchain.agents import ZeroShotAgent, AgentExecutor
from langchain.memory import ConversationBufferWindowMemory

import logging
from api.chain_tools import load_tools


class ArcGISTutor:
    def __init__(self, llm_type="openai", session_id="my-session"):
        logging.info("loading ArcGISTutor")
        self.__set_llm__(llm_type)
        self.redis_url = os.getenv("REDIS_URL")
        self.session_id = session_id

    def __set_llm__(self, llm_type="openai"):
        if llm_type == "openai":
            self.llm = OpenAI(temperature=0)
            self.model = ChatOpenAI(temperature=0)
        elif llm_type == "azure":
            self.llm = AzureOpenAI(temperature=0)
            self.model = AzureChatOpenAI(temperature=0)
        else:
            raise ValueError("llm_type must be 'openai' or 'azure'")

    def get_prompt(self, tools):
        tool_names = ", ".join([tool.name for tool in tools])
        
        prefix = """Have a conversation with a ArcGIS User, answering the following questions as best you can. You have access to the following tools:"""
        format = f"""
            Use the following format:

            Question: the input question you must answer
            Thought: you should always think about what to do
            Action: the action to take, should be one of [{tool_names}]]
            Action Input: the input to the action
            Observation: the result of the action
            ... (this Thought/Action/Action Input/Observation can repeat N times)
            Thought: I now know the final answer
            Final Answer: the final answer to the original input question
        """
        suffix = format + """Begin!"

        {chat_history}
        Question: {input}
        {agent_scratchpad}"""

        prompt = ZeroShotAgent.create_prompt(
            tools,
            prefix=prefix,
            suffix=suffix,
            input_variables=["input", "chat_history", "agent_scratchpad"],
        )
        return prompt

    def agent(self):
        tools = load_tools(self.llm)
        message_history = RedisChatMessageHistory(
            url=self.redis_url, ttl=600, session_id=self.session_id
        )
        prompt = self.get_prompt(tools)
        memory = ConversationBufferWindowMemory(k=5, return_messages=True, chat_memory=message_history)
        llm_chain = LLMChain(llm = self.llm, prompt=prompt, verbose=True)
        agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True)
        agent_chain = AgentExecutor.from_agent_and_tools(
            agent=agent, tools=tools, memory=memory
        )
        # agent_chain = PlanAndExecute(
        #     planner=planner,
        #     executor=executor,
        #     verbose=True,
        #     prompt=self.prompts(),
        #     memory=memory,
        # )
        return agent_chain


tutor = ArcGISTutor()
agent = tutor.agent()

if __name__ == "__main__":
    agent.run(
        "What is ArcGIS?",
    )
