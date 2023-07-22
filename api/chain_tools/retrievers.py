from .utils import load_vectorstore
import json

def get_retrievers(prompt):
    retrivers = []
    with open('api/retrievers.json', 'r') as f:
        retrivers = json.load(f)
        
        for config in retrivers:
            retriver = load_vectorstore(config["retriever"])
            config["retriever"] = retriver.as_retriever()
            config["prompt"] = prompt
    return retrivers

# def get_code_retrievers():
#     retrivers = []
#     with open('api/code_retrievers.json', 'r') as f:
#         retrivers = json.load(f)
        
#         for config in retrivers:
#             retriver = load_vectorstore(config["retriever"])
#             config["retriever"] = retriver.as_retriever()
#             config["retriever"].search_kwargs["distance_metric"] = "cos"
#             config["retriever"].search_kwargs["fetch_k"] = 20
#             config["retriever"].search_kwargs["maximal_marginal_relevance"] = True
#             config["retriever"].search_kwargs["k"] = 20
#     return retrivers