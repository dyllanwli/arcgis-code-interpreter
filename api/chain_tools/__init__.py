from .tools import *


def load_tools(llm, memory=None):
    print("loading tools")
    return [
        documentation_tool(llm),
        shapefile_analysis(llm),
        general_assitant(llm, memory=memory),
    ]
    
    
    