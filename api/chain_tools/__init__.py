from .tools import *

def load_tools(llm, memory=None):
    return [
        documentation_tool(llm),
        math_tool(llm),
        general_assitant(llm, memory=memory),
        arcgis_code_sample(llm)
    ]
    
    
    