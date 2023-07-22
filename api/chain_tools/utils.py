import logging
import pickle
from pathlib import Path
from typing import Optional


def load_vectorstore(vectorstore_path: Optional[str] = "api/storage/vectorstore.pkl"):
    logging.info("loading vectorstore")
    vectorstore = None
    if not Path(vectorstore_path).exists():
        raise ValueError("vectorstore.pkl does not exist, please run ingest.py first")
    with open(vectorstore_path, "rb") as f:
        vectorstore = pickle.load(f)
    return vectorstore