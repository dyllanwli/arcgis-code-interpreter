from .tools import *

def load_tools(llm):
    return [
        documentation_tool(llm),
        math_tool(llm),
    ]
    
    
    