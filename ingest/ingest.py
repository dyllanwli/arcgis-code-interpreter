"""Load html from files, clean up, split, ingest into Weaviate."""
import pickle

# from langchain.document_loaders import ReadTheDocsLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from langchain.document_loaders import WebBaseLoader

import os

def ingest_docs(documents_path: str, output_path: str):
    # Read the document_link.txt file
    with open(documents_path, "r") as f:
        document_links = f.readlines()
        
    document_links = [link.strip() for link in document_links]
    
    print("Reading {} documents".format(len(document_links)))
    # Put the document_link into webbaseloader
    loader = WebBaseLoader(document_links)
    

    raw_documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    documents = text_splitter.split_documents(raw_documents)
    # add deploument if want to use azure
    # deployment = os.getenv("DEPLOYMENT")
    embeddings = OpenAIEmbeddings()
    print("documents", documents)
    vectorstore = FAISS.from_documents(documents, embeddings)

    # Save vectorstore
    with open(output_path, "wb") as f:
        pickle.dump(vectorstore, f)
    

def ingest_resources():
    """Get documents from web pages."""
    
    resources_path = "./resources"
    output_file_prefix = "../api/storage/"
    
    # read add txt file from resources_path
    for file in os.listdir(resources_path):
        if file.endswith(".txt"):
            print("Ingesting {}".format(file))
            documents_path = os.path.join(resources_path, file)
            output_path = output_file_prefix + file.split(".")[0] + ".pkl"
            print("Output path: {}".format(output_path))
            ingest_docs(documents_path, output_path)
    
import os
from dotenv import load_dotenv
load_dotenv()
print("Running on API_BASE:", os.getenv("OPENAI_API_BASE"))

if __name__ == "__main__":
    ingest_resources()
