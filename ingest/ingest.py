"""Load html from files, clean up, split, ingest into Weaviate."""
import pickle

from langchain.document_loaders import ReadTheDocsLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from langchain.document_loaders import WebBaseLoader



def ingest_docs():
    """Get documents from web pages."""
    
    # Read the document_link.txt file
    with open("document_link.txt", "r") as f:
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
    embeddings = OpenAIEmbeddings()
    print("documents", documents)
    vectorstore = FAISS.from_documents(documents, embeddings)

    # Save vectorstore
    with open("../api/storage/vectorstore.pkl", "wb") as f:
        pickle.dump(vectorstore, f)


if __name__ == "__main__":
    ingest_docs()
