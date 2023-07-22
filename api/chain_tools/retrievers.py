from .utils import load_vectorstore



def get_retrievers():
    retrivers = [
        {
            "name": "ArcGIS Pro Documentation",
            "description": "Good for answering questions about the ArcGIS Pro",
            "retriever": "api/storage/arcgis_pro.pkl"
        },
        {
            "name": "ArcGIS Rest API Documentation",
            "description": "Good for answering questions about the ArcGIS Rest API",
            "retriever": "api/storage/arcgis_rest_api.pkl"
        },
    ]
    for config in retrivers:
        retriver = load_vectorstore(config["retriever"])
        config["retriever"] = retriver.as_retriever()
    return retrivers